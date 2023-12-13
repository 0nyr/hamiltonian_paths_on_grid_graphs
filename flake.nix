{
  description = "All my python packages in one place.";

  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixos-unstable;
    research-base.url = "github:0nyr/research-base";
  };

  outputs = { self, nixpkgs, research-base, ... }: 
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    pythonPackages = pkgs.python311Packages;

    impurePythonEnv = pkgs.mkShell rec {
      name = "impurePythonEnv";
      venvDir = "./.venv";
      buildInputs = [
        pythonPackages.python
        pythonPackages.venvShellHook
        pkgs.autoPatchelfHook

        pythonPackages.python-dotenv
        pythonPackages.psutil
        pythonPackages.pandas
        pythonPackages.numpy
        pythonPackages.seaborn
        pythonPackages.matplotlib
        pythonPackages.datetime

        pythonPackages.pandas-stubs
        pythonPackages.types-psutil

        # animation
        pkgs.manim
        pythonPackages.manimpango

        # image processing
        pythonPackages.pillow
        
        # graphs
        pkgs.graphviz # for tools like sfdp
        pythonPackages.graphviz
        pythonPackages.pygraphviz
        pythonPackages.pydot # needed with networkx
        pythonPackages.networkx
      ];

      postVenvCreation = ''
        unset SOURCE_DATE_EPOCH
        pip install -r requirements.txt
        autoPatchelf ./venv
      '';

      postShellHook = ''
        unset SOURCE_DATE_EPOCH
      '';
    };

  in {
      # Expose the environment as a default package
      defaultPackage.x86_64-linux = impurePythonEnv;
    };
}
