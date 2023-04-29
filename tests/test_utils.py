from entities.entity import Entity


def test_equal(a, b):
    return a == b


def test_not_none(a):
    return a is not None


def assert_equal(a, b, test_results, options={}):
    default_options = {"fail": False}
    options = {**default_options, **options}

    result = test_equal(a, b)

    # if the test has already failed, don't bother
    if not result:
        # map bad result to the gold value
        recovery_results = test_results.get("recovered_results", {})
        recovery_results[a.data.get("value")] = b
        test_results["recovered_results"] = recovery_results
        failed_items = test_results.get("failed_items", set())
        failed_items.add(b.data.get("value"))
        test_results["failed_items"] = failed_items

        # increment the failure count
        total_failures = test_results.get("total_failures", 0)
        total_failures += 1
        test_results["total_failures"] = failures

        unique_failure = not (
            isinstance(b, Entity)
            and b.data.get("value") in test_results.get("failed_items", {})
        )
        if unique_failure:
            failures = test_results.get("failures", 0)
            failures += 1
            test_results["failures"] = failures

        # document the failure
        result = {
            "message": f"{a} != {b}",
            "unique_failure": unique_failure,
            "test": a,
            "gold": b,
        }
        results = test_results.get("results", [])
        results.append(result)
        test_results["results"] = results

        if options.get("fail"):
            raise AssertionError(result)


def assert_not_none(a, test_results, options={}):
    default_options = {"fail": False}
    options = {**default_options, **options}

    result = test_not_none(a)

    # if the test has already failed, don't bother
    if not result:
        # increment the failure count
        total_failures = test_results.get("total_failures", 0)
        total_failures += 1
        test_results["total_failures"] = failures

        failures = test_results.get("failures", 0)
        failures += 1
        test_results["failures"] = failures

        # document the failure
        result = {
            "message": f"{a} is None",
            "unique_failure": True,
            "test": a,
        }
        results = test_results.get("results", [])
        results.append(result)
        test_results["results"] = results

        if options.get("fail"):
            raise AssertionError(result)


def assert_test(test_results):
    if test_results.get("failures", 0) > 0:
        message = f"""
            {test_results.get("failures")} failures (total failures: {test_results.get("total_failures")})): 
            {[result.get("message", "Test failed") for result in test_results.get("results", [])]}
        """
        raise AssertionError(message)
