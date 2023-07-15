def test_setupcall():
    """
    Test the call of the setup function
    """
    import os
    import jupyter_nestdesktop_proxy as jx

    os.environ["NESTDESKTOP_BIN"] = "nest-desktop"

    print("\nRunning test_setupcall...")
    print(jx.setup_nestdesktop())
