#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests [very sensitive to pytest output]

Summary:	pytest fixture for benchmarking code
Summary(pl.UTF-8):	Wyposażenie pytesta do testowania wydajności kodu
Name:		python3-pytest-benchmark
Version:	5.1.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-benchmark/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-benchmark/pytest-benchmark-%{version}.tar.gz
# Source0-md5:	66a8040a2bc0813be44680d4b4254882
URL:		https://github.com/ionelmc/pytest-benchmark
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:30.3.0
%if %{with tests}
#BuildRequires:	python3-aspectlib >= 2.0.0
# for storage tests
#BuildRequires:	python3-elasticsearch >= 8.15.1
BuildRequires:	python3-freezegun >= 1.5.1
BuildRequires:	python3-py-cpuinfo
# for histogram tests
#BuildRequires:	python3-pygal >= 3.0.5
#BuildRequires:	python3-pygaljs >= 1.0.2
BuildRequires:	python3-pytest >= 8.1
# ?
#BuildRequires:	python3-hunter
#BuildRequires:	python3-nbmake >= 1.5.4
#BuildRequires:	python3-pytest-instafail >= 0.5.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	sphinx-pdg-3 >= 1.3
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A py.test fixture for benchmarking code. It will group the tests into
rounds that are calibrated to the chosen timer.

%description -l pl.UTF-8
Wyposażenie (fixture) modułu py.test do testowania wydajności kodu.
Grupuje testy w rundy, które są kalibrowane do wybranego stopera.

%package apidocs
Summary:	API documentation for Python pytest_benchmark module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest_benchmark
Group:		Documentation

%description apidocs
API documentation for Python pytest_benchmark module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest_benchmark.

%prep
%setup -q -n pytest-benchmark-%{version}

# (mostly temporarily disabled tests)
# requires elasticsearch
%{__rm} tests/test_elasticsearch_storage.py
# no py.test-benchmark program before install
%{__rm} tests/test_cli.py
# requires pygal for histograms
%{__rm} tests/test_storage.py
# require aspectlib
%{__rm} tests/test_with_testcase.py
%{__rm} tests/test_with_weaver.py
# a few too depending on git, one elasticsearch
%{__rm} tests/test_utils.py
# requires nbmake
%{__sed} -i -e '/--nbmake/d' pytest.ini

%build
%py3_build

%if %{with tests}
# test_histogram requires pygal,pygaljs
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_benchmark.plugin,xdist.plugin \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -k 'not test_histogram'
%endif

%if %{with doc}
cd docs
PYTHONPATH=$(pwd)/../src \
sphinx-build-3 -b html . _build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/py.test-benchmark{,-3}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pytest-benchmark{,-3}
ln -s py.test-benchmark-3 $RPM_BUILD_ROOT%{_bindir}/py.test-benchmark
ln -s pytest-benchmark-3 $RPM_BUILD_ROOT%{_bindir}/pytest-benchmark

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/py.test-benchmark
%attr(755,root,root) %{_bindir}/pytest-benchmark
%attr(755,root,root) %{_bindir}/py.test-benchmark-3
%attr(755,root,root) %{_bindir}/pytest-benchmark-3
%{py3_sitescriptdir}/pytest_benchmark
%{py3_sitescriptdir}/pytest_benchmark-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_modules,_static,*.html,*.js}
%endif
