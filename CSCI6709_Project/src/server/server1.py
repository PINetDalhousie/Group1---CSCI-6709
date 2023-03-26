import flwr as fl

fl.server.start_server(server_address='10.0.0.2:8080', config=fl.server.ServerConfig(num_rounds=3))