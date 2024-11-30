# test_sensor_reader.py

from read_sensors import LogicHandler

def test_logic_handler_with_dummy_data():
    # Create an instance of LogicHandler (which internally uses SensorManager)
    logic_handler = LogicHandler()

    # Connect to sensors (simulated)
    logic_handler.connect_to_sensors()

    # Fetch XYZ data using dummy values
    logic_handler.sensor_manager.update_sensors(use_dummy=True)

    # Fetch and print external and internal XYZ data
    external_xyz = (logic_handler.sensor_manager.total_x_external, 
                    logic_handler.sensor_manager.total_y_external, 
                    logic_handler.sensor_manager.total_z_external)
    
    internal_xyz = (logic_handler.sensor_manager.total_x_internal, 
                    logic_handler.sensor_manager.total_y_internal, 
                    logic_handler.sensor_manager.total_z_internal)

    print("External XYZ Data:", external_xyz)
    print("Internal XYZ Data:", internal_xyz)

    # Calculate and print magnitudes
    external_magnitude = logic_handler.calculate_magnitude(external_xyz)
    internal_magnitude = logic_handler.calculate_magnitude(internal_xyz)

    print("External Magnitude:", external_magnitude)
    print("Internal Magnitude:", internal_magnitude)

    # Close the sensors (cleanup)
    logic_handler.close_sensors()

# Run the test
if __name__ == "__main__":
    test_logic_handler_with_dummy_data()
