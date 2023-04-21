from prefect import task, flow


@task
def test_func():
    print("HELLO WORLD")


@flow(
    name="example-default-docker",
    log_prints=True,
)
def main():
    test_func()


if __name__ == "__main__":
    main()
