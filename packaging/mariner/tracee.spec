Name:		tracee
Version:	VERSION
Release:	RELEASE
License:	MIT
Summary:	Security and forensics tool with a runtime detection engine.
BuildRequires:	llvm
BuildRequires:	clang
BuildRequires:	golang
BuildRequires:	make
BuildRequires:	elfutils-libelf-devel
BuildRequires:	zlib-devel
BuildRoot:	../../
Packager:	Mark Dalton Gray <graymark@microsoft.com>
URL:		https://github.com/aquasecurity/tracee
Source:		/tracee/tracee

%description
Tracee eBPF is a security and forensics tool. It uses Linux eBPF technology to
trace your system and applications at runtime, and analyzes collected events to
detect suspicious behavioral patterns. Use it with tracee-rules to have a
complete security runtime detection system. Tracee rules is a security
detection engine and receives events from Tracee eBPF and, according to defined
signatures (REGO or Golang), warn about suspicious behavior.

%package ebpf
Summary: Security and forensics tool.
Requires: elfutils-libelf
Requires: zlib-devel

%description ebpf
Tracee eBPF is a security and forensics tool. It uses Linux eBPF technology to
trace your system and applications at runtime, and analyzes collected events to
detect suspicious behavioral patterns. Use it with tracee-rules to have a
complete security runtime detection system.

%package rules
Summary: Runtime detection engine.
Requires: tracee-ebpf = %{version}-%{release}

%description rules
Tracee rules is a security detection engine and receives events from Tracee
eBPF and, according to defined signatures (REGO or Golang), warn about
suspicious behavior.

# fedora 34, 35 and 36 only, and they don't need btfhub support
%build
make clean
BTFHUB=0 make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_libdir}

# tracee-ebpf
mkdir -m 0755 -p $RPM_BUILD_ROOT/%{_bindir}
install -m 0755 ./dist/tracee-ebpf $RPM_BUILD_ROOT/%{_bindir}
# tracee-rules
mkdir -m 0755 -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -m 0755 -p $RPM_BUILD_ROOT/%{_libdir}/tracee
install -m 0755 ./dist/tracee-rules $RPM_BUILD_ROOT/%{_libdir}/tracee
ln -s %{_libdir}/tracee/tracee-rules $RPM_BUILD_ROOT/%{_bindir}/tracee-rules
# rules
mkdir -m 0755 -p $RPM_BUILD_ROOT/%{_libdir}/tracee/rules/
install -m 0644 ./dist/rules/* $RPM_BUILD_ROOT/%{_libdir}/tracee/rules/

%clean

%files -n tracee-ebpf
%{_bindir}/tracee-ebpf

%files -n tracee-rules
%{_bindir}/tracee-rules
%{_libdir}/tracee/*
