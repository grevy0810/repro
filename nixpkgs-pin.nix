let
  rev = "1b31087ac11ac1d2634ed938dd4761a917288938";
  sha256 = "0zhnqvkl1qw8apxx20g1p2qhbph6q37qgggnp3zqcp9i4hknaymd";
in
import (builtins.fetchTarball {
  url = "https://github.com/NixOS/nixpkgs/archive/${rev}.tar.gz";
  inherit sha256;
})
