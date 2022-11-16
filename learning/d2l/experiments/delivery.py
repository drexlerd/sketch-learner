from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="delivery",
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain="domain",
    )

    exps["sketch_debug"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instances=training_instances(),
        debug_features=["n_count(c_not(c_equal(r_primitive(at_g,0,1),r_primitive(at,0,1))))",  # 5
                        "b_empty(c_primitive(empty,0))",  # 2
                        "n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(truck,0)), r_primitive(adjacent,0,1), c_primitive(at_g,1))",  # 7
                        "n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(truck,0)), r_primitive(adjacent,0,1), c_and(c_all(r_inverse(r_primitive(at_g,0,1)),c_bot),c_some(r_inverse(r_primitive(at,0,1)),c_primitive(package,0))))",  # 15
                        # "n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(truck,0)),r_primitive(adjacent,0,1),c_not(c_all(r_inverse(r_primitive(at,0,1)),c_equal(r_primitive(at,0,1),r_primitive(at_g,0,1)))))" alternative feature
        ],
    )

    exps["sketch"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instances=training_instances(),
        max_states_per_instance=2000,
    )

    exps["hierarchy"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        instances=training_instances(),
        # instances=["instance_3_2_3"],
        max_states_per_instance=2000,
    )

    exps["hierarchy_debug"] = update_dict(
        strips_base,
        pipeline="debug_hierarchy_pipeline",
        sketch="(:policy\n"
               "(:boolean_features )\n"
               "(:numerical_features \"n_count(r_and(r_primitive(at,0,1),r_primitive(at_g,0,1)))\")\n"
               "(:rule (:conditions ) (:effects (:e_n_inc 0)))\n"
               ")",
        policy="(:policy\n"
               "(:boolean_features \"b_empty(r_primitive(carrying,0,1))\")\n"
               "(:numerical_features \"n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(truck,0)),r_primitive(adjacent,0,1),c_some(r_inverse(r_primitive(at,0,1)),c_primitive(package,0)))\" \"n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(truck,0)),r_primitive(adjacent,0,1),c_some(r_inverse(r_primitive(at_g,0,1)),c_top))\")\n"
               "(:rule (:conditions (:c_b_neg 0) (:c_n_eq 1) (:c_n_gt 0)) (:effects (:e_b_pos 0) (:e_n_bot 1) (:e_n_dec 0)))\n"
               "(:rule (:conditions (:c_b_neg 0) (:c_n_gt 1)) (:effects (:e_b_bot 0) (:e_n_dec 1) (:e_n_inc 0)))\n"
               "(:rule (:conditions (:c_b_pos 0) (:c_n_eq 0) (:c_n_gt 1)) (:effects (:e_b_neg 0) (:e_n_bot 0) (:e_n_bot 1)))\n"
               "(:rule (:conditions (:c_b_pos 0) (:c_n_eq 0) (:c_n_gt 1)) (:effects (:e_b_neg 0) (:e_n_bot 1) (:e_n_inc 0)))\n"
               "(:rule (:conditions (:c_b_pos 0) (:c_n_gt 0)) (:effects (:e_b_bot 0) (:e_n_dec 0) (:e_n_inc 1)))\n"
               "(:rule (:conditions (:c_b_pos 0) (:c_n_gt 1)) (:effects (:e_b_bot 0) (:e_n_bot 0) (:e_n_dec 1)))\n"
               "(:rule (:conditions (:c_n_gt 0) (:c_n_gt 1)) (:effects (:e_b_bot 0) (:e_n_dec 0) (:e_n_dec 1)))\n"
               ")",
        instances=["instance_4_1_0"],
        max_states_per_instance=2000,
    )
    return exps


def training_instances():
    return [f"instance_{i}_{j}_{k}" for i in range(2,5) for j in range(1,3) for k in range(0,10) ]
