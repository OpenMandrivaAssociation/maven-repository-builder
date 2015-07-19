%{?_javapackages_macros:%_javapackages_macros}
Name:           maven-repository-builder
Version:        1.0
Release:        1.2
# Maven-shared defines maven-repository-builder version as 1.0
Epoch:          1
Summary:        Maven repository builder
Group:		Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-repository-builder/

Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/maven-repository-builder/1.0/maven-repository-builder-%{version}-source-release.zip
# ASL mandates that the licence file be included in redistributed source
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  junit
BuildRequires:  maven-local
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-test-tools
BuildRequires:	maven-wagon
#BuildRequires:  maven-wagon-file
#BuildRequires:  maven-wagon-http-lightweight
BuildRequires:  maven-shared

Obsoletes:      maven-shared-repository-builder < %{epoch}:%{version}-%{release}
Provides:       maven-shared-repository-builder = %{epoch}:%{version}-%{release}

%description
Maven repository builder.

This is a replacement package for maven-shared-repository-builder

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
    
%description javadoc
API documentation for %{name}.


%prep
%setup -q

# Replace plexus-maven-plugin with plexus-component-metadata
find -name 'pom.xml' -exec sed \
    -i 's/<artifactId>plexus-maven-plugin<\/artifactId>/<artifactId>plexus-component-metadata<\/artifactId>/' '{}' ';'
find -name 'pom.xml' -exec sed \
    -i 's/<goal>descriptor<\/goal>/<goal>generate-metadata<\/goal>/' '{}' ';'

# Removing JARs because of binary code contained
find -iname '*.jar' -delete

cp %{SOURCE1} LICENSE.txt

%build
# Skipping tests because they don't work without the JARs
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt


%changelog
* Mon Nov 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-1
- Update to upstream version 1.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-0.9.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:1.0-0.8.alpha2
- Use Requires: java-headless rebuild (#1067528)

* Thu Feb 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-0.7.alpha2
- Migrate to Wagon subpackages

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-0.6.alpha2
- Fix unowned directory

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

