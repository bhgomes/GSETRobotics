import robotapi as ri


@ri.whileloop(ri.STOP, ri.safe_exit, "exit")
def run():
    ri.test_sensor_value()

run()
