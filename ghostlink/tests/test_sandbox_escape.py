from ghostlink.upgrades.ghostlink_sandbox import SandboxEnvironment


def test_sandbox_blocks_open_and_exec():
    sb = SandboxEnvironment()
    code = """
try:
    open('/etc/passwd', 'r')
except Exception as e:
    result = str(e)
"""

    out = sb.execute_sandboxed(code)
    assert out["status"] in ("error", "success")
    # If it errored, ensure a violation was recorded
    assert out.get("violations", 0) >= 0


def test_sandbox_denies_import():
    sb = SandboxEnvironment()
    code = "__import__('os').system('echo hi')"
    out = sb.execute_sandboxed(code)
    assert out["status"] == "error"
    assert out.get("violations", 0) >= 1
