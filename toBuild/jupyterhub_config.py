import pwd, subprocess
c = get_config()
# Setting better authenticator
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"
# Adding admin user
c.Authenticator.admin_users = {"admin"}
# Adding spawner hook to create user jupyter workspace
def hook(sp):
    name = sp.user.name
    try:
        pwd.getpwnam(name)
    except KeyError:
        subprocess.check_call(['useradd', '-ms', '/bin/bash', name])
# Setting hook
c.Spawner.pre_spawn_hook = hook
