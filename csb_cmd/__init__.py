from csb_cmd.common import *
from csb_cmd import git, admin
#from csb_cmd.open import open_impl
#from csb_cmd.hash import hash_impl

client.add_cog(git.git_impl);
client.add_cog(admin.admin_impl);
#client.add_cog(open_impl);
#client.add_cog(hash_impl);
