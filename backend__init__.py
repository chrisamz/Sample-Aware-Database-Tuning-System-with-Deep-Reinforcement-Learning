# backend/__init__.py

from .data_collector import DataCollector
from .db_connector import DBConnector
from .rl_agent import RLAgent
from .parameter_adjuster import ParameterAdjuster

def initialize_system(db_config, rl_config):
    """
    Initializes the database tuning system with the given configurations.

    Args:
        db_config (dict): Configuration for the database connection.
        rl_config (dict): Configuration for the reinforcement learning agent.

    Returns:
        tuple: Instances of DataCollector, DBConnector, RLAgent, and ParameterAdjuster.
    """
    # Initialize database connector
    db_connector = DBConnector(db_config)

    # Initialize data collector
    data_collector = DataCollector(db_connector)

    # Initialize RL agent
    rl_agent = RLAgent(rl_config)

    # Initialize parameter adjuster
    parameter_adjuster = ParameterAdjuster(db_connector, rl_agent)

    return data_collector, db_connector, rl_agent, parameter_adjuster

def start_monitoring(data_collector, parameter_adjuster, interval=60):
    """
    Starts the monitoring and tuning process.

    Args:
        data_collector (DataCollector): Instance of DataCollector.
        parameter_adjuster (ParameterAdjuster): Instance of ParameterAdjuster.
        interval (int): Time interval (in seconds) between each monitoring cycle.
    """
    import time
    while True:
        # Collect performance data
        performance_data = data_collector.collect_data()

        # Adjust parameters based on the performance data
        parameter_adjuster.adjust_parameters(performance_data)

        # Wait for the next cycle
        time.sleep(interval)
