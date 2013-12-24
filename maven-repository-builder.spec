%_javapackages_macros
%global pkg_version 1.0-alpha-2

Name:           maven-repository-builder
Version:        1.0
# See http://fedoraproject.org/wiki/Packaging:NamingGuidelines#Package_Versioning
Release:        0.5.alpha2.0%{?dist}
# Maven-shared defines maven-repository-builder version as 1.0
Epoch:          1
Summary:        Maven repository builder
License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-repository-builder/

# svn export http://svn.apache.org/repos/asf/maven/shared/tags/maven-repository-builder-1.0-alpha-2 maven-repository-builder-1.0-alpha-2
# tar caf maven-repository-builder-1.0-alpha-2.tar.xz maven-repository-builder-1.0-alpha-2/
Source0:        %{name}-%{pkg_version}.tar.xz
# ASL mandates that the licence file be included in redistributed source
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildArch:      noarch

BuildRequires:  easymock3
BuildRequires:  java-devel
BuildRequires:  junit
BuildRequires:  maven-local
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-test-tools
BuildRequires:  maven-wagon
BuildRequires:  maven-shared

Obsoletes:      maven-shared-repository-builder < %{epoch}:%{version}-%{release}
Provides:       maven-shared-repository-builder = %{epoch}:%{version}-%{release}

%description
Maven repository builder.

This is a replacement package for maven-shared-repository-builder

%package javadoc

Summary:        Javadoc for %{name}
    
%description javadoc
API documentation for %{name}.


%prep
%setup -q -n %{name}-%{pkg_version}

# Replace plexus-maven-plugin with plexus-component-metadata
find -name 'pom.xml' -exec sed \
    -i 's/<artifactId>plexus-maven-plugin<\/artifactId>/<artifactId>plexus-component-metadata<\/artifactId>/' '{}' ';'
find -name 'pom.xml' -exec sed \
    -i 's/<goal>descriptor<\/goal>/<goal>generate-metadata<\/goal>/' '{}' ';'

# Removing JARs because of binary code contained
find -iname '*.jar' -delete

cp %{SOURCE1} LICENSE.txt

# Migrate from easymock 1 to easymock 3
%pom_remove_dep easymock:
%pom_add_dep org.easymock:easymock:3.2:test

%build
# Skipping tests because they don't work without the JARs
%mvn_build -f

%install
%mvn_install
%if 0%{?fedora}
%else
# rpm5 parser...
sed -i 's|1.0-alpha-2|1.0.alpha.2|g;' %{buildroot}%{_mavendepmapfragdir}/*
%endif

%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt


%changelog
* Thu Aug 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-0.5.alpha2
- Migrate from easymock 1 to easymock 3
- Resolves: rhbz#1002478

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-0.4.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Tomas Radej <tradej@redhat.com> - 1:1.0-0.3.alpha2
- Added BR on maven-shared

* Fri Feb 08 2013 Tomas Radej <tradej@redhat.com> - 1:1.0-0.2.alpha2
- Removed bundled JAR
- Building the new way

* Fri Jan 11 2013 Tomas Radej <tradej@redhat.com> - 1:1.0-0.1.alpha2
- Initial version

