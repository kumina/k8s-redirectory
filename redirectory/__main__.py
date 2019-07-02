"""
The main entry point of the application.
Depending on the configuration that is provided it will invoke
different starting points of the application.

Based on the node type different runnables will be invoked.
There are three type of runnables:
    WorkerService
    ManagementService
    CompilerJob
All of them inherit from runnable and have the run method implemented.
"""


def main():
    from kubi_ecs_logger import Logger, Severity
    from redirectory.libs_int.config import Configuration

    # Get configurations
    config = Configuration().values

    # Setup logging based on config
    log_level_str = str(config.log_level).upper()
    Logger().dev = config.deployment == "dev"
    Logger().severity_output_level = Severity[log_level_str]

    # Log loaded configuration
    Logger().event(
        category="configuration",
        action="configuration loaded",
        dataset=Configuration().path
    ).out(severity=Severity.INFO)

    # Map runners to node_types from configuration
    from redirectory.runnables import ManagementService, WorkerService, CompilerJob
    run_map = {
        "management": ManagementService,
        "worker": WorkerService,
        "compiler": CompilerJob
    }

    # Import all models and services
    import redirectory.models
    import redirectory.services

    # Run application
    run_map[Configuration().values.node_type]().run()


if __name__ == "__main__":
    # STOPPED USING RE LOADER
    # import sys
    # import os
    # Fix path because of Flask dev server reloaded is not able to find module redirectory
    # sys.path.append(os.getcwd())
    main()
