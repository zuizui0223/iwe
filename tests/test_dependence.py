import pandas as pd

from iwe.dependence import (
    validate_dependency_registry,
    validate_effect_dependency_assignments,
)


def _registry():
    return pd.DataFrame(
        [
            {
                "study_id": "IWE001",
                "dependency_status": "confirmed",
                "required_dependence_id": "DEP_CORYDALIS",
                "scope": "programme",
                "notes": "",
            },
            {
                "study_id": "IWE002",
                "dependency_status": "confirmed",
                "required_dependence_id": "DEP_CORYDALIS",
                "scope": "programme",
                "notes": "",
            },
            {
                "study_id": "IWE003",
                "dependency_status": "unresolved",
                "required_dependence_id": None,
                "scope": "programme",
                "notes": "",
            },
        ]
    )


def _effects(dependence_id="DEP_CORYDALIS", study_id="IWE001"):
    return pd.DataFrame(
        [
            {
                "effect_id": "E1",
                "study_id": study_id,
                "dependence_id": dependence_id,
            }
        ]
    )


def test_confirmed_dependency_assignment_passes():
    assert validate_effect_dependency_assignments(_effects(), _registry()) == []


def test_wrong_registered_dependency_id_fails():
    errors = validate_effect_dependency_assignments(
        _effects(dependence_id="DEP_INDEPENDENT"),
        _registry(),
    )
    assert any("requires dependence_id=DEP_CORYDALIS" in error for error in errors)


def test_future_iwe002_effect_must_inherit_same_cluster():
    errors = validate_effect_dependency_assignments(
        _effects(study_id="IWE002", dependence_id="DEP_IWE002"),
        _registry(),
    )
    assert any("study IWE002 requires dependence_id=DEP_CORYDALIS" in error for error in errors)


def test_unresolved_registry_row_cannot_preassign_cluster():
    registry = _registry()
    registry.loc[registry["study_id"] == "IWE003", "required_dependence_id"] = "DEP_GUESS"
    errors = validate_dependency_registry(registry)
    assert any("unresolved dependency rows" in error for error in errors)
