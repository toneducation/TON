
{ pkgs }: {
  deps = [
    pkgs.python3Full
    pkgs.python3Packages.pip
    pkgs.python3Packages.python-dotenv
    pkgs.python3Packages.requests
    pkgs.python3Packages.python-telegram-bot
  ];
}
