#
# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Microsoft Windows namke file which builds the cmockery library and example 
# applications.
#
# To use this makefile...
# Select Start->Run and run "cmd.exe" to open the command line.
# Run "vsvars.bat" located in Microsoft Visual Studio's directory.
# Run "nmake" to build the cmockery library and example applications.
# Run "nmake clean" to delete all files built by this makefile.

LIBRARY_SOURCE_DIRECTORY=..\src
EXAMPLE_SOURCE_DIRECTORY=..\src\example

CFLAGS=/nologo /c /D_WIN32_WINNT=0x501 /I$(LIBRARY_SOURCE_DIRECTORY)\google \
	/I$(EXAMPLE_SOURCE_DIRECTORY)
CC_COMMAND=$(CC) $(CFLAGS) $(**) /Fo$(@)
CC_COMMAND_UNIT_TEST=$(CC_COMMAND) /DUNIT_TESTING=1

LIBLINKFLAGS=/NOLOGO /MACHINE:x86 /SUBSYSTEM:console

LIBRARY_ARCHIVER=lib.exe
LIBFLAGS=$(LIBLINKFLAGS)
LIB_COMMAND=$(LIBRARY_ARCHIVER) $(LIBFLAGS) $(**) /OUT:$(@)

LINK=link.exe
LFLAGS=$(LIBLINKFLAGS) libcmt.lib kernel32.lib /NODEFAULTLIB:libc.lib
LINK_COMMAND=$(LINK) $(LFLAGS) $(**) /OUT:$(@)

.SUFFIXES: .exe .lib .obj .c

all: cmockery.lib calculator.exe calculator_test.exe allocate_module_test.exe \
	assert_macro_test.exe customer_database_test.exe key_value_test.exe \
	product_database_test.exe run_tests.exe

clean:
	-cmd /c "@for %A in (\
		cmockery.lib cmockery.obj \
		calculator.exe calculator.obj \
		calculator_test.exe calculator_test.obj \
			calculator_test-calculator.obj \
		allocate_module_test.exe allocate_module_test.obj \
			allocate_module.obj \
		assert_macro_test.exe assert_macro_test.obj \
			assert_macro.obj \
		customer_database_test.exe customer_database_test.obj \
			customer_database.obj \
		key_value_test.exe key_value_test.obj key_value.obj \
		product_database_test.exe product_database_test.obj \
			product_database.obj \
		run_tests.exe run_tests.obj) do @del %A 2>NUL"

# Rules for the cmockery library.
cmockery.lib: cmockery.obj
cmockery.obj: $(LIBRARY_SOURCE_DIRECTORY)\cmockery.c

# Rules for the calculator application.
calculator.exe: calculator.obj

calculator.obj: $(EXAMPLE_SOURCE_DIRECTORY)\calculator.c
	$(CC_COMMAND)

# Rules for the calculator test application.
calculator_test.exe: calculator_test.obj calculator_test-calculator.obj \
                     cmockery.lib
	$(LINK_COMMAND)

calculator_test.obj: $(EXAMPLE_SOURCE_DIRECTORY)\calculator_test.c

calculator_test-calculator.obj: $(EXAMPLE_SOURCE_DIRECTORY)\calculator.c
	$(CC_COMMAND_UNIT_TEST)

# Sample code applications.
allocate_module_test.exe: allocate_module_test.obj allocate_module.obj \
		cmockery.lib
	$(LINK_COMMAND)

allocate_module_test.obj: $(EXAMPLE_SOURCE_DIRECTORY)\allocate_module_test.c
allocate_module.obj: $(EXAMPLE_SOURCE_DIRECTORY)\allocate_module.c

assert_macro_test.exe: assert_macro_test.obj assert_macro.obj \
		cmockery.lib
	$(LINK_COMMAND)

assert_macro_test.obj: $(EXAMPLE_SOURCE_DIRECTORY)\assert_macro_test.c
assert_macro.obj: $(EXAMPLE_SOURCE_DIRECTORY)\assert_macro.c

customer_database_test.exe: customer_database_test.obj customer_database.obj \
		cmockery.lib
	$(LINK_COMMAND)

customer_database_test.obj: \
		$(EXAMPLE_SOURCE_DIRECTORY)\customer_database_test.c
customer_database.obj: $(EXAMPLE_SOURCE_DIRECTORY)\customer_database.c

key_value_test.exe: key_value_test.obj key_value.obj \
		cmockery.lib
	$(LINK_COMMAND)

key_value_test.obj: $(EXAMPLE_SOURCE_DIRECTORY)\key_value_test.c
key_value.obj: $(EXAMPLE_SOURCE_DIRECTORY)\key_value.c

product_database_test.exe: product_database_test.obj product_database.obj \
		cmockery.lib
	$(LINK_COMMAND)

product_database_test.obj: $(EXAMPLE_SOURCE_DIRECTORY)\product_database_test.c
product_database.obj: $(EXAMPLE_SOURCE_DIRECTORY)\product_database.c

run_tests.exe: run_tests.obj cmockery.lib
	$(LINK_COMMAND)

run_tests.obj: $(EXAMPLE_SOURCE_DIRECTORY)\run_tests.c

# Inference rules.
.obj.exe:
	$(LINK_COMMAND)

.obj.lib:
	$(LIB_COMMAND)

{$(LIBRARY_SOURCE_DIRECTORY)\}.c{}.obj:
	$(CC_COMMAND)

{$(EXAMPLE_SOURCE_DIRECTORY)\}.c{}.obj:
	$(CC_COMMAND_UNIT_TEST)
