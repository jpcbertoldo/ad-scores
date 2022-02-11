from collections import defaultdict
from dataclasses import dataclass
from email.policy import default
from enum import Enum
import traceback
from typing import Dict, List, Optional, Set, Tuple, Union
import warnings
from numpy import ndarray
from pandas import DataFrame
from pybtex.database.input import bibtex
from pathlib import Path

from adscores import constants
from adscores.data import fcdd_2021_table2


PAPERS_BIB_FPATH = Path(__file__).parent / "papers.bib"


bib_parser = bibtex.Parser()
bib_data = bib_parser.parse_file(str(PAPERS_BIB_FPATH))


class MissingInfo(KeyError):
    pass


class UnknownDataset(Exception):
    pass


class UnknownMetric(Exception):
    pass


class DatasetKey(Enum):
    mvtecad = "MVTec-AD"
    cifar10 = "CIFAR-10"
    cifar100 = "CIFAR-100"
    fmnist = "Fashion-MNIST"
    imagenet30ad = "ImageNet30AD"
    imagenet1k = "ImageNet1k"
    
    @staticmethod
    def names() -> Tuple[str]:
        return tuple(e.name for e in DatasetKey)
    
    @staticmethod
    def values() -> Tuple[str]:
        return tuple(e.value for e in DatasetKey)
    

DATASETS_CLASSES_ABC = {
    DatasetKey.mvtecad: constants.MVTECAD_CLASSES_ABC,
    DatasetKey.cifar10: constants.CIFAR10_CLASSES_ABC,
    DatasetKey.imagenet30ad: constants.IMAGENET_30AD_CLASSES_ABC,
    DatasetKey.fmnist: constants.FMNIST_CLASSES_ABC,
}
DATASETS_CLASSES_ABC = {k.value: v for k, v in DATASETS_CLASSES_ABC.items()}
    
    
class MetricKey(Enum):
    pixel_wise_auroc = "pixel_wise_auroc"
    
    @staticmethod
    def names() -> Tuple[str]:
        return tuple(e.name for e in MetricKey)
    
    @staticmethod
    def values() -> Tuple[str]:
        return tuple(e.value for e in MetricKey)


class SupervisionKey(Enum):
    unsupervised = "unsupervised"
    semi_supervised = "semi-supervised"
    supervised = "supervised"
    self_supervised = "self-supervised"

    
class TagKey(Enum):
    
    src = "source"
    src_detail = "source-detail"
    # where the numbers where actually taken from by the source
    # not necessarily the paper where the method was published
    src_original = "source-original"  
    
    method = "method"
    method_ref = "method-reference"
    method_abbr = "method-abbreviation"
    
    dataset = "dataset"
    dataset_ref = "dataset-reference"
    
    metric = "metric"
    metric_perclass = "metric-per-class"
    metric_percentage = "metric-percentage"
    # number of experiences that were averaged to get the score value
    metric_niter = "metric-number-of-iterations"  
    
    oe = "outlier-exposure"
    pretraining = "pretraining"
    supervision = "supervision"

    
REFERENCE_TAGKEYS = (
    TagKey.src,
    TagKey.src_original,
    TagKey.method_ref,
    TagKey.dataset_ref,
)
    
    
class TagValues(Enum):
    yes = "yes"
    no = "no"
    

@dataclass
class Tag:
    
    key: TagKey
    value: str
    
    def __post_init__(self):
        if isinstance(self.value, Enum):
            self.value = self.value.value
    
    
@dataclass
class Score:
    
    value: Union[int, float, ndarray, DataFrame] = None
    tags: Tuple[Tag] = ()
    
    def __post_init__(self):
        # make sure the tag keys are unique
        tagkeys = set()
        for tag in self.tags:
            assert isinstance(tag, Tag), f"{tag=}"
            assert isinstance(tag.key, TagKey), f"{tag.key=}"
            if tag.key in tagkeys:
                raise KeyError(f"Tag key {tag.key} already exists. Tags must be unique. Tags: {self.tags}")
            tagkeys.add(tag.key)
     
    @property
    def tag_keys(self) -> Set[str]:
        return {tag.key for tag in self.tags}
     
    def __getitem__(self, key: TagKey) -> str:
        assert isinstance(key, TagKey)
        for tag in self.tags:
            if tag.key == key:
                return tag.value
        else:
            raise MissingInfo(f"Tag key {key=} not found in {self.tags=}")
        
    def tags_as_dict(self) -> dict:
        return {tag.key.value: tag.value for tag in self.tags}
        

SCORES = []

# =============================================================================
# from liznerski_explainable_2021
# Liznerski, P., Ruff, L., Vandermeulen, R.A., Franks, B.J., Kloft, M., Muller, K.R., 2021. Explainable Deep One-Class Classification, in: International Conference on Learning Representations. Presented at the International Conference on Learning Representations.
# Table 3
# =============================================================================


SCORES.extend([
    Score(
        value=fcdd_2021_table2.get_aess(),
        tags=(
            Tag(key=TagKey.src, value="liznerski_explainable_2021"),
            Tag(key=TagKey.src_detail, value="Table 2"),
            Tag(key=TagKey.src_original, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.method, value="Scores for Self-Similarity"),
            Tag(key=TagKey.method_abbr, value="AE-SS"),
            Tag(key=TagKey.method_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.dataset, value=DatasetKey.mvtecad),
            Tag(key=TagKey.dataset_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.metric, value=MetricKey.pixel_wise_auroc),
            Tag(key=TagKey.metric_perclass, value=TagValues.yes),
        )
    ),
    Score(
        value=fcdd_2021_table2.get_ael2(),
        tags=(
            Tag(key=TagKey.src, value="liznerski_explainable_2021"),
            Tag(key=TagKey.src_detail, value="Table 2"),
            Tag(key=TagKey.src_original, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.method, value="L2 Autoencoder"),
            Tag(key=TagKey.method_abbr, value="AE-L2"),
            Tag(key=TagKey.method_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.dataset, value=DatasetKey.mvtecad),
            Tag(key=TagKey.dataset_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.metric, value=MetricKey.pixel_wise_auroc),
            Tag(key=TagKey.metric_perclass, value=TagValues.yes),
        )
    ),
    Score(
        value=fcdd_2021_table2.get_ano_gan(),
        tags=(
            Tag(key=TagKey.src, value="liznerski_explainable_2021"),
            Tag(key=TagKey.src_detail, value="Table 2"),
            Tag(key=TagKey.src_original, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.method, value="AnoGAN"),
            Tag(key=TagKey.method_abbr, value="AnoGAN"),
            Tag(key=TagKey.method_ref, value="schlegl_unsupervised_2017"),
            Tag(key=TagKey.dataset, value=DatasetKey.mvtecad),
            Tag(key=TagKey.dataset_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.metric, value=MetricKey.pixel_wise_auroc),
            Tag(key=TagKey.metric_perclass, value=TagValues.yes),
        )
    ),
    Score(
        value=fcdd_2021_table2.get_cnnfd(),
        tags=(
            Tag(key=TagKey.src, value="liznerski_explainable_2021"),
            Tag(key=TagKey.src_detail, value="Table 2"),
            Tag(key=TagKey.src_original, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.method, value="CNN Feature Dictionaries"),
            Tag(key=TagKey.method_abbr, value="CNNFD"),
            Tag(key=TagKey.method_ref, value="napoletano_anomaly_2018"),
            Tag(key=TagKey.dataset, value=DatasetKey.mvtecad),
            Tag(key=TagKey.dataset_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.metric, value=MetricKey.pixel_wise_auroc),
            Tag(key=TagKey.metric_perclass, value=TagValues.yes),
        )
    ),
    Score(
        value=fcdd_2021_table2.get_vevae(),
        tags=(
            Tag(key=TagKey.src, value="liznerski_explainable_2021"),
            Tag(key=TagKey.src_detail, value="Table 2"),
            Tag(key=TagKey.src_original, value="liu_towards_2020"),
            Tag(key=TagKey.method, value="Visually Explained Variational Autoencoder"),
            Tag(key=TagKey.method_abbr, value="VEVAE"),
            Tag(key=TagKey.method_ref, value="liu_towards_2020"),
            Tag(key=TagKey.dataset, value=DatasetKey.mvtecad),
            Tag(key=TagKey.dataset_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.metric, value=MetricKey.pixel_wise_auroc),
            Tag(key=TagKey.metric_perclass, value=TagValues.yes),
        )
    ),
    Score(
        value=fcdd_2021_table2.get_smai(),
        tags=(
            Tag(key=TagKey.src, value="liznerski_explainable_2021"),
            Tag(key=TagKey.src_detail, value="Table 2"),
            Tag(key=TagKey.src_original, value="li_superpixel_2020"),
            Tag(key=TagKey.method, value="Superpixel Masking and Inpainting"),
            Tag(key=TagKey.method_abbr, value="SMAI"),
            Tag(key=TagKey.method_ref, value="li_superpixel_2020"),
            Tag(key=TagKey.dataset, value=DatasetKey.mvtecad),
            Tag(key=TagKey.dataset_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.metric, value=MetricKey.pixel_wise_auroc),
            Tag(key=TagKey.metric_perclass, value=TagValues.yes),
        )
    ),
    Score(
        value=fcdd_2021_table2.get_gdr(),
        tags=(
            Tag(key=TagKey.src, value="liznerski_explainable_2021"),
            Tag(key=TagKey.src_detail, value="Table 2"),
            Tag(key=TagKey.src_original, value="dehaene_iterative_2020"),
            Tag(key=TagKey.method, value="Gradient Descent Reconstruction with VAEs"),
            Tag(key=TagKey.method_abbr, value="GDR"),
            Tag(key=TagKey.method_ref, value="dehaene_iterative_2020"),
            Tag(key=TagKey.dataset, value=DatasetKey.mvtecad),
            Tag(key=TagKey.dataset_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.metric, value=MetricKey.pixel_wise_auroc),
            Tag(key=TagKey.metric_perclass, value=TagValues.yes),
        )
    ),
    Score(
        value=fcdd_2021_table2.get_pnet(),
        tags=(
            Tag(key=TagKey.src, value="liznerski_explainable_2021"),
            Tag(key=TagKey.src_detail, value="Table 2"),
            Tag(key=TagKey.src_original, value="zhou_encoding_2020"),
            Tag(key=TagKey.method, value="Encoding Structure-Texture Relation with P-Net for AD"),
            Tag(key=TagKey.method_abbr, value="P-NET"),
            Tag(key=TagKey.method_ref, value="zhou_encoding_2020"),
            Tag(key=TagKey.dataset, value=DatasetKey.mvtecad),
            Tag(key=TagKey.dataset_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.metric, value=MetricKey.pixel_wise_auroc),
            Tag(key=TagKey.metric_perclass, value=TagValues.yes),
        )
    ),
    Score(
        value=fcdd_2021_table2.get_fcdd_unsupervised(),
        tags=(
            Tag(key=TagKey.src, value="liznerski_explainable_2021"),
            Tag(key=TagKey.src_detail, value="Table 2"),
            Tag(key=TagKey.method, value="Fully Convolutional Data Description (unsupervised)"),
            Tag(key=TagKey.method_abbr, value="FCDD-unsup"),
            Tag(key=TagKey.method_ref, value="liznerski_explainable_2021"),
            Tag(key=TagKey.dataset, value=DatasetKey.mvtecad),
            Tag(key=TagKey.dataset_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.metric, value=MetricKey.pixel_wise_auroc),
            Tag(key=TagKey.metric_perclass, value=TagValues.yes),
            Tag(key=TagKey.metric_niter, value="5"),
        )
    ),
    Score(
        value=fcdd_2021_table2.get_fcdd_semi_supervised(),
        tags=(
            Tag(key=TagKey.src, value="liznerski_explainable_2021"),
            Tag(key=TagKey.src_detail, value="Table 2"),
            Tag(key=TagKey.method, value="Fully Convolutional Data Description (semi-supervised)"),
            Tag(key=TagKey.method_abbr, value="FCDD-semi-sup"),
            Tag(key=TagKey.method_ref, value="liznerski_explainable_2021"),
            Tag(key=TagKey.dataset, value=DatasetKey.mvtecad),
            Tag(key=TagKey.dataset_ref, value="bergmann_mvtec_2019"),
            Tag(key=TagKey.metric, value=MetricKey.pixel_wise_auroc),
            Tag(key=TagKey.metric_perclass, value=TagValues.yes),
            Tag(key=TagKey.metric_niter, value="5"),
        )
    ),
])

# =============================================================================
# UTIL FUNCTIONS
# =============================================================================


def get_dataset(score: Score) -> str:
    return score[TagKey.dataset]


def get_metric(score: Score) -> str:
    return score[TagKey.metric]
    

def score_is_perclass(score: Score, assume_no=True) -> bool:
    return score[TagKey.metric_perclass] == TagValues.yes.value


def get_dataset_classes_abc(score: Score) -> Tuple[str]:
    
    dataset_key = score[TagKey.dataset]
    
    try:
        return DATASETS_CLASSES_ABC[dataset_key]
    
    except KeyError as ex:
        raise UnknownDataset(f"Unknown dataset classes {dataset_key=}. {score.tags=}") from ex 


def _validate_and_normalize_dataset(dataset: Union[DatasetKey, str]) -> str:
    
    if isinstance(dataset, DatasetKey):
        return dataset.value
    
    elif isinstance(dataset, str):
        
        if dataset in DatasetKey.names():
            return DatasetKey[dataset].value
        
        elif dataset in DatasetKey.values():
            return dataset
        
        else:
            raise UnknownDataset(f"Unknown dataset {dataset=}")
    
    else:
        raise TypeError(f"Expected {DatasetKey=} or {str=}, got {type(dataset)=}")


def _validate_and_normalize_metric(metric: Union[MetricKey, str]) -> str:
    
    if isinstance(metric, MetricKey):
        return metric.value
    
    elif isinstance(metric, str):
        
        if metric in MetricKey.names():
            return MetricKey[metric].value
        
        elif metric in MetricKey.values():
            return metric
        
        else:
            raise UnknownMetric(f"Unknown metric {metric=}")
    
    else:
        raise TypeError(f"Expected {MetricKey=} or {str=}, got {type(metric)=}")


def get_perclass_scores(dataset: Union[DatasetKey, str], metric: Union[MetricKey, str]) -> DataFrame:
    dataset = _validate_and_normalize_dataset(dataset)
    metric = _validate_and_normalize_metric(metric)
    return [
        s for s in SCORES
        if score_is_perclass(s) 
        and get_dataset(s) == dataset
        and get_metric(s) == metric
    ]
    
    
def score_perclass_2_records(score: Score) -> List[dict]:
    assert score_is_perclass(score), f"Expected per-class score, got {score.tags=}"
    # score.value is expected to be a DataFrame with one column "score"
    # and the index is the class names
    return [
        {
            "class": idx,
            "score": row["score"],
            **score.tags_as_dict(),
        }
        for idx, row in score.value.iterrows()
    ]

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================


def _get_unknown_refs(scores: List[Score]) -> List[str]:

    unknown_refs = set()

    for s in scores:
        refs = [
            t.value 
            for t in s.tags 
            if t.key in REFERENCE_TAGKEYS
        ]
        
        for r in refs:
            if r not in bib_data.entries.keys():
                unknown_refs.add(r)

    return sorted(list(unknown_refs))


def _get_missing_values(scores: List[Score]) -> List[str]:

    missing_values = set()

    for idx, s in enumerate(scores):
        if s.value is None:
            missing_values.add(idx)

    return sorted(list(missing_values))

    
def validate_scores_perclass(scores: List[Score]) -> None:
    
    for idx, s in enumerate(scores):
        
        if not score_is_perclass(s, assume_no=True):
            continue        
        
        try:
            dataset_classes_abc = get_dataset_classes_abc(s)
        
        except UnknownDataset as ex:
            traceback.print_exc()
            raise ex

        df: DataFrame = s.value
        
        if df is None:
            warnings.warn(f"Score per class is None. Skipping. {idx=} {s.tags=}")
            print("\n\n")
            continue
        
        elif not isinstance(df, DataFrame):
            warnings.warn(f"Score per class is not a DataFrame. Skipping. {idx=} {s.tags=}")
            print("\n\n")
            continue
        
        if not tuple(df.index.values) == dataset_classes_abc:
            warnings.warn(f"Classes in score per class is wrong. Skipping. {idx=} {s.tags=}")
            print("\n\n")
            continue


def validate_metrics(scores: List[Score]) -> None:
    
    for idx, s in enumerate(scores):
        
        try:
            _validate_and_normalize_metric(get_metric(s))
        
        except (UnknownMetric, MissingInfo) as ex:
            print(f"{idx=} {s.tags=}")
            traceback.print_exc()
    
        
def validate_datasets(scores: List[Score]) -> None:
    
    for idx, s in enumerate(scores):
        
        try:
            _validate_and_normalize_dataset(get_dataset(s))
        
        except (UnknownDataset, MissingInfo) as ex:
            print(f"{idx=} {s.tags=}")
            traceback.print_exc()
            
        
# =============================================================================
# MAIN
# =============================================================================


if __name__ == "__main__":

    unknown_refs = _get_unknown_refs(SCORES)
    
    if len(unknown_refs) > 0:
        warnings.warn(f"Unknown refs: {', '.join(unknown_refs)}")
    
    missing_values = _get_missing_values(SCORES)
    
    if len(missing_values) > 0:
        warnings.warn(f"Missing values (index of the score in the list SCORES): {', '.join(map(str, missing_values))}")

    validate_datasets(SCORES)
    validate_metrics(SCORES)
    validate_scores_perclass(SCORES)
    
    