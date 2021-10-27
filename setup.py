from setuptools import setup, find_packages


def get_requirements():
    requirements_list = []

    with open("requirements.txt") as reqs:
        for install in reqs:
            requirements_list.append(install.strip())

    return requirements_list


def get_packages_and_requirements():
    reqs = get_requirements()

    exclude = ["whatsapp.support*"]
    packs = find_packages(exclude=exclude)

    return packs, reqs


def main():
    packages, requirements = get_packages_and_requirements()

    setup(
        name="wa-terminal",
        version="0.1",
        packages=packages,
        url="https://github.com/afikrim/wa-terminal",
        license="",
        author="afikrim",
        author_email="afikrim10@gmail.com",
        description="Whatsapp using terminal",
        install_requires=requirements,
    )


if __name__ == "__main__":
    main()
