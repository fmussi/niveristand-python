from niveristand import nivs_rt_sequence, NivsParam, realtimesequencetools
from niveristand.clientapi import BooleanValue, ChannelReference, DoubleValue
from niveristand.library import wait

""" This module contains a basic example of how to create an RT sequence in Python.

Refer to the MBSE demo example.
"""
RTSEQPDESTPATH = "C:\\azdo\\mst-adg-scs.e2mRoadshow\\demos\\mbse\\src\\Automation"


# You must mark RT sequences with the following decorator:
@nivs_rt_sequence
# You must also specify parameter data types, default values, and whether to pass parameters by value or by reference.
@NivsParam("enable", BooleanValue(0), NivsParam.BY_REF)
@NivsParam("setpoint_rpm", DoubleValue(0), NivsParam.BY_REF)
def mbse_demo_basic(enable, setpoint_rpm):
    """Turn on the engine, set the desired_rpm to the passed value for 20 seconds, and shut down the engine.

    You must access parameters through their ".value" property.
    """
    # You can access a channel with a ChannelReference
    enable_chan = ChannelReference("Aliases/Controller/Enable")
    dsetpoint_rpm_chan = ChannelReference("Aliases/Controller/Speed Setpoint (RPM)")
    enable_chan.value = enable.value
    dsetpoint_rpm_chan.value = setpoint_rpm.value
    wait(DoubleValue(20))
    enable_chan.value = False
    dsetpoint_rpm_chan.value = 0


@nivs_rt_sequence
def run_mbse_demo():
    """Sets up channel references and calls the actual test."""
    # You can call an RT sequence the same way you call a normal Python function.
    # However, if you pass functions by reference, you must create strongly-typed objects.
    mbse_demo_basic(BooleanValue(True), DoubleValue(2500))


def run_non_deterministic():
    """Runs the sequence non-deterministically.

    This function executes the RT Sequence on the host using the public ClientAPI
    that installs with VeriStand. This function communicates with the gateway to set and get channel values.

    If you use a Python integrated developer environment (IDE),
    you can debug this function like a normal Python function.
    """
    run_mbse_demo()


def run_deterministic():
    """Compiles the sequence and runs it deterministically inside the VeriStand engine.

    You cannot use debugging tools at this stage because VeriStand executes the sequence, not Python.
    If you do not mark the functions as @nivs_rt_sequence, Python will raise a :any:`niveristand.errors.VeristandError`.
    """
    # The run_py_as_rtseq function accepts, as a parameter, the Python function you want to call as an RT sequence.
    realtimesequencetools.run_py_as_rtseq(run_mbse_demo)


if __name__ == "__main__":
    realtimesequencetools.save_py_as_rtseq(run_mbse_demo, RTSEQPDESTPATH)
    run_non_deterministic()
    print("Finished non-deterministic")
    run_deterministic()
    print("Finished deterministic")
