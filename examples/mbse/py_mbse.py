# import modules used here -- sys is a very standard one
import argparse
import logging
import niveristand.legacy.NIVeriStand as NIVeriStand
from niveristand.errors import RunError

ALIAS_TO_TEST = "Aliases/Controller/Speed Feedback (RPM)"


def test_execution_api(sysdef_path, deploy_flag):
    workspace = NIVeriStand.Workspace2("localhost")
    print("")
    if deploy_flag is True:
        print("Deploying %s" % sysdef_path)
        workspace.ConnectToSystem(sysdef_path, True, 20000)

    try:
        test_value = workspace.GetSingleChannelValue(ALIAS_TO_TEST)
        print("Value of {0} is : {1}".format(ALIAS_TO_TEST, test_value))
    except RunError as e:
        print("Error: %d -  %s" % (int(e.error.error_code), e.error.message))

    finally:
        if deploy_flag is True:
            workspace.DisconnectFromSystem("", 1)


# Gather our code in a main() function
def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    # TODO Replace this with your actual code.
    print("Test API example.")
    test_execution_api(args.sysdef_path, args.deploy)


# Standard boilerplate to call the main() function to begin
# the program.


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Does a thing to some stuff.",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars="@",
    )
    # TODO Specify your real parameters here.
    parser.add_argument(
        "-s",
        "--sysdef_path",
        help="System Definition file path",
        metavar="PATH",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--deploy",
        help="Deploy flag. Set true to deploy sysdef file",
        metavar="DEPLOY",
        required=False,
    )
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
