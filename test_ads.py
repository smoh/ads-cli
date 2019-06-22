import pytest
from click.testing import CliRunner

from ads_cli import cli


def test_export():
    runner = CliRunner()

    result = runner.invoke(cli, ["export", "2005IAUS..216..170H"])
    assert result.exit_code == 0
    assert (
        result.output.strip()
        == """@INPROCEEDINGS{2005IAUS..216..170H,
       author = {{Huchra}, J. and {Martimbeau}, N. and {Jarrett}, T. and {Cutri}, R. and
         {Skrutskie}, M. and {Schneider}, S. and {Steining}, R. and {Macri}, L. and
         {Mader}, J. and {George}, T.},
        title = "{2MASS and the Nearby Universe}",
    booktitle = {Maps of the Cosmos},
         year = "2005",
       editor = {{Colless}, Matthew and {Staveley-Smith}, Lister and
         {Stathakis}, Raylee A.},
       series = {IAU Symposium},
       volume = {216},
        month = "Jan",
        pages = {170},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2005IAUS..216..170H},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}"""
    )

    result = runner.invoke(cli, ["export", "'2013A&A...558A..33A'"])
    assert result.exit_code == 0
