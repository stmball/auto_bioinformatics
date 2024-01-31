from flask import Flask, request, jsonify, send_file
from cStringIO import StringIO
import pandas as pd
import typing as tp

import src.imputers as imputers
import src.normalisers as normalisers
import src.reducers as reducers
import src.scalers as scalers
from src.analysis import AutoAnalysis, AutoAnalysisConfig
from src.reporting import Reporter


app = Flask(__name__)


@app.route("/api")
def index():
    return "Hello World!"


@app.route("/api/list_preprocessors")
def list_preprocessors():
    return jsonify(
        {
            "scalers": [scaler.name for scaler in scalers.Scaler.__subclasses__()],
            "normalisers": [
                normaliser.name
                for normaliser in normalisers.Normaliser.__subclasses__()
            ],
            "reducers": [reducer.name for reducer in reducers.Reducer.__subclasses__()],
            "imputers": [imputer.name for imputer in imputers.Imputer.__subclasses__()],
        }
    )


@app.route("/api/analyze", methods=["POST"])
def analyze():
    # Get the JSON data from the POST request
    data = request.get_json()

    # Get the config from the JSON data
    config = parse_config(data["config"])

    # Get the data from the JSON data
    data = parse_data(data["data"])

    # Run the analysis
    analysis = AutoAnalysis(data, config)

    analysis.run()

    report = Reporter(analysis, output_path=None).report()

    f = StringIO()
    report.report.save(f)
    f.seek(0)
    return send_file(
        f,
        as_attachment=True,
        attachment_filename="report.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    return jsonify(analysis_json)


def parse_config(config):
    if config["groups"]:
        groups = config["groups"].split(",")
    else:
        raise ValueError("No groups given.")

    if config["gene_sets"]:
        gene_sets = config["gene_sets"].split(",")
    else:
        gene_sets = ["KEGG_2019_Human", "MSigDB_Hallmark_2020"]

    if config["scaler"]:
        scaler = get_preprocessor(config["scaler"], scalers.Scaler)
    else:
        scaler = scalers.Log2Scaler()

    if config["imputer"]:
        imputer = get_preprocessor(config["imputer"], imputers.Imputer)
    else:
        imputer = imputers.KNN_Imputer()

    if config["normaliser"]:
        normaliser = get_preprocessor(config["normaliser"], normalisers.Normaliser)
    else:
        normaliser = normalisers.PowerScaler()

    if config["reducer"]:
        reducer = get_preprocessor(config["reducer"], reducers.Reducer)
    else:
        reducer = reducers.PCA_Reducer()

    return AutoAnalysisConfig(
        groups=groups,
        gene_name_col=config["gene_col"] if config["gene_col"] else "Gene",
        p_value_threshold=config["p_value_threshold"]
        if config["p_value_threshold"]
        else 0.05,
        log_fold_change_threshold=config["log_fold_change_threshold"]
        if config["log_fold_change_threshold"]
        else 1,
        gene_sets=gene_sets,
        organism=config["organism"] if config["organism"] else "Human",
        plot_dir=config["plot_dir"] if config["plot_dir"] else "./img",
        output_dir=config["output_dir"] if config["output_dir"] else "./out",
        scaler=scaler,
        imputer=imputer,
        normaliser=normaliser,
        reducer=reducer,
    )


def get_preprocessor(
    name: str,
    baseclass: tp.Union[
        scalers.Scaler, imputers.Imputer, normalisers.Normaliser, reducers.Reducer
    ],
) -> scalers.Scaler:
    """Return the scaler with the given name."""
    classes = baseclass.__subclasses__()
    for preprocessor in classes:
        if preprocessor.name == name:
            return preprocessor()

    raise ValueError(f"{name} not found. Options are: {[c.name for c in classes]}")


def parse_data(data):
    return pd.io.json.json_normalize(data)


if __name__ == "__main__":
    app.run(debug=True)
