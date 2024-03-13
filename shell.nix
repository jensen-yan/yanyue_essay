{pkgs ? import <nixpkgs> {}}:
let
  name = "ucasproposal";
  myPython = pkgs.python3.withPackages (p: with p; [
    ipython
    matplotlib
    pandas
    numpy
    openpyxl
    scipy
    jinja2
  ]);
in
pkgs.mkShell {
  inherit name;
  packages = with pkgs; [
    texliveFull
    myPython
    librsvg
    pandoc
  ];
  shellHook = ''
    # env
    export PYTHONPATH=${myPython}/${myPython.sitePackages}
    export debian_chroot=${name}
  '';
}
