class RadialPowerFlow:
    def __init__(self, line_data, v_slack_kv=12.66, s_base_kva = 1000.0):
        self.v_slack = v_slack_kv
        self.s_base = s_base_kva # 1000 kVA = 1MW
        self.v_base = v_slack_kv
        self.z_base = (self.s_base ** 2) / (self.s_base / 1000.0) # base impedance in Ohms

        # Build network tree structure
        self.parents = {}
        self.children = {i : [] for i in range(0, 33)}
        self.r_pu = {}

        for data in line_data.values():
            f, t, r_ohm = data["from"], data["to"], data["r"]
            f-=1
            t-=1
            self.parents[t] = f
            self.children[f].append(t)
            self.r_pu[(f,t)] = r_ohm / self.z_base

        # Determine topological sweep order (substation downstream to leaves)
        self.sweep_order = self.__get_sweep_order()

    def __get_sweep_order(self):
        # BFS queue traversal to order nodes by depth.
        order = []
        queue = [1]
        while queue:
            node = queue.pop(0)
            order.append(node)
            queue.extend(self.children[node])
        return order


    def solve(self, grid_kv, max_iter=20, tolerance=1e-5):
        # Solves power flow using active power (P) and computes voltage profile
        # Convert loads and generation to per-unit

        p_inj_pu = {i: grid_kv[i] / self.s_base for i in range(0, 33)}

        # Initialize all node voltages to 1.0 p.u (flat start)
        voltages = {i: 1.0 for i in range(0, 33)}
        flows = {}

        for i in range(max_iter):
            v_old = voltages.copy()

            # 1. Backwards sweep: calculate branch flows (leaves to root)
            flows = {}
            for node in reversed(self.sweep_order):
                if node == 0:
                    continue
                parent = self.parents[node]

                # Flow on branch (parent -> node) is local net load + sum of downstream branch flows
                local_net_demand_pu = -p_inj_pu[node]
                downstream_flow_pu = sum(flows.get((node, child), 0.0) for child in self.children[node])
                flows[(parent, node)] = local_net_demand_pu + downstream_flow_pu

            # 2. Forward sweep: update node voltages (root to leaves)
            voltages[0] = 1.0 # slack bus voltage remains constant
            for parent in self.sweep_order:
                for child in self.children[parent]:
                    r_pu = self.r_pu[(parent, child)]
                    p_flow_pu = flows.get((parent, child), 0.0)

                    # Compute downstream voltage drop
                    voltages[child] = voltages[parent] - (r_pu * p_flow_pu) / voltages[parent]

            # Check convergence (max change in voltage)
            max_error = max(abs(voltages[i] - v_old[i]) for i in range(0, 33))
            if max_error < tolerance:
                break

        # Convert back to physical units
        voltages_kv = {node: self.v_base - (v * self.v_base) for node, v in voltages.items()}
        slack_kw = sum(flows.get((0, child), 0.0) for child in self.children[0]) * self.s_base
        return voltages_kv, slack_kw