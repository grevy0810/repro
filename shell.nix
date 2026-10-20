let
  pkgs = import ./nixpkgs-pin.nix {};
in
pkgs.mkShell {
  packages = [
    pkgs.jdk21
  ];
}
