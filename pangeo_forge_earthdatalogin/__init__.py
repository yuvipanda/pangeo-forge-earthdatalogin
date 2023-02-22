import netrc
import os

import aiohttp
from pangeo_forge_recipes.transforms import OpenURLWithFSSpec


class OpenURLWithEarthDataLogin(OpenURLWithFSSpec):
    def expand(self, *args, **kwargs):
        auth_kwargs = {}
        if "EARTHDATA_LOGIN_TOKEN" in os.environ:
            auth_kwargs = {
                "headers": {"Authorization": f'Bearer {os.environ["EARTHDATA_LOGIN_TOKEN"]}'}
            }
        elif os.path.exists(os.environ.get("NETRC", os.path.expanduser("~/.netrc"))):
            # FIXME: Actually support the NETRC environment variable
            username, _, password = netrc.netrc().authenticators("urs.earthdata.nasa.gov")
            if username:
                auth_kwargs = {"auth": aiohttp.BasicAuth(username, password)}
        if auth_kwargs:
            if self.open_kwargs is None:
                self.open_kwargs = auth_kwargs
            else:
                self.open_kwargs.update(auth_kwargs)
        else:
            raise ValueError(
                "No earthdata login credentials found - set a token with EARTHDATA_LOGIN_TOKEN environment variable, or an entry for urs.earthdata.nasa.gov in your netrc file"
            )
        return super().expand(*args, **kwargs)
