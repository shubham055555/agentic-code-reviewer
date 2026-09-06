from evaluation.metrics import calculate_metrics


def test_metrics():

    result = calculate_metrics(
        true_positives=8,
        false_positives=2,
        false_negatives=2,
    )

    assert result["true_positives"] == 8
    assert result["false_positives"] == 2
    assert result["false_negatives"] == 2

    assert result["precision"] == 0.8
    assert result["recall"] == 0.8
    assert result["f1"] == 0.8
