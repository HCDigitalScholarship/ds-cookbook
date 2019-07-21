## Status Inactive UFW

I ran into some trouble configuring nginx after install using [this](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04?utm_source=local&utm_medium=Email_Internal&utm_campaign=Email_UbuntuDistroNginxWelcome&mkt_tok=eyJpIjoiT0RnMFlUZzBPR1JqWlRBeCIsInQiOiJ6QlVYejR2OEJDREwxc0V6dmgyT0NrY3VcL3NIMzhwZjBtTzhMTFwvNSsralZzbHZYblwvNURlMDkwaFI3R1lzQnNINkxoXC9lZTZpUDZ4UXdpajNxY2N3UVVRdnNzQ2JcL0I1TUprUldhYWYzeUNqRVgrb211WmM1c0psOFQxcU1RSG5DIn0%3D).

What fixed it was `sudo ufw enable` after I received the response "Status: inactive" from running `sudo ufw status`. [Source](https://www.digitalocean.com/community/questions/sudo-ufw-status-return-inactive)

Then I added `sudo ufw allow 'OpenSSH'` to match the status response in the tutorial.
