# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Default target executed when no arguments are given to make.
default_target: all

.PHONY : default_target

# Allow only one "make -f Makefile2" at a time, but pass parallelism.
.NOTPARALLEL:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /mnt/c/users/chris/onedrive/desktop/summerofbrain

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /mnt/c/users/chris/onedrive/desktop/summerofbrain

#=============================================================================
# Targets provided globally by CMake.

# Special rule for the target install/strip
install/strip: preinstall
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Installing the project stripped..."
	/usr/bin/cmake -DCMAKE_INSTALL_DO_STRIP=1 -P cmake_install.cmake
.PHONY : install/strip

# Special rule for the target install/strip
install/strip/fast: preinstall/fast
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Installing the project stripped..."
	/usr/bin/cmake -DCMAKE_INSTALL_DO_STRIP=1 -P cmake_install.cmake
.PHONY : install/strip/fast

# Special rule for the target install/local
install/local: preinstall
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Installing only the local directory..."
	/usr/bin/cmake -DCMAKE_INSTALL_LOCAL_ONLY=1 -P cmake_install.cmake
.PHONY : install/local

# Special rule for the target install/local
install/local/fast: preinstall/fast
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Installing only the local directory..."
	/usr/bin/cmake -DCMAKE_INSTALL_LOCAL_ONLY=1 -P cmake_install.cmake
.PHONY : install/local/fast

# Special rule for the target test
test:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Running tests..."
	/usr/bin/ctest --force-new-ctest-process $(ARGS)
.PHONY : test

# Special rule for the target test
test/fast: test

.PHONY : test/fast

# Special rule for the target list_install_components
list_install_components:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Available install components are: \"Unspecified\""
.PHONY : list_install_components

# Special rule for the target list_install_components
list_install_components/fast: list_install_components

.PHONY : list_install_components/fast

# Special rule for the target edit_cache
edit_cache:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "No interactive CMake dialog available..."
	/usr/bin/cmake -E echo No\ interactive\ CMake\ dialog\ available.
.PHONY : edit_cache

# Special rule for the target edit_cache
edit_cache/fast: edit_cache

.PHONY : edit_cache/fast

# Special rule for the target rebuild_cache
rebuild_cache:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Running CMake to regenerate build system..."
	/usr/bin/cmake -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR)
.PHONY : rebuild_cache

# Special rule for the target rebuild_cache
rebuild_cache/fast: rebuild_cache

.PHONY : rebuild_cache/fast

# Special rule for the target install
install: preinstall
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Install the project..."
	/usr/bin/cmake -P cmake_install.cmake
.PHONY : install

# Special rule for the target install
install/fast: preinstall/fast
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Install the project..."
	/usr/bin/cmake -P cmake_install.cmake
.PHONY : install/fast

# The main all target
all: cmake_check_build_system
	$(CMAKE_COMMAND) -E cmake_progress_start /mnt/c/users/chris/onedrive/desktop/summerofbrain/CMakeFiles /mnt/c/users/chris/onedrive/desktop/summerofbrain/CMakeFiles/progress.marks
	$(MAKE) -f CMakeFiles/Makefile2 all
	$(CMAKE_COMMAND) -E cmake_progress_start /mnt/c/users/chris/onedrive/desktop/summerofbrain/CMakeFiles 0
.PHONY : all

# The main clean target
clean:
	$(MAKE) -f CMakeFiles/Makefile2 clean
.PHONY : clean

# The main clean target
clean/fast: clean

.PHONY : clean/fast

# Prepare targets for installation.
preinstall: all
	$(MAKE) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall

# Prepare targets for installation.
preinstall/fast:
	$(MAKE) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall/fast

# clear depends
depend:
	$(CMAKE_COMMAND) -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 1
.PHONY : depend

#=============================================================================
# Target rules for targets named SummerOfBrain

# Build rule for target.
SummerOfBrain: cmake_check_build_system
	$(MAKE) -f CMakeFiles/Makefile2 SummerOfBrain
.PHONY : SummerOfBrain

# fast build rule for target.
SummerOfBrain/fast:
	$(MAKE) -f CMakeFiles/SummerOfBrain.dir/build.make CMakeFiles/SummerOfBrain.dir/build
.PHONY : SummerOfBrain/fast

#=============================================================================
# Target rules for targets named gmock_main

# Build rule for target.
gmock_main: cmake_check_build_system
	$(MAKE) -f CMakeFiles/Makefile2 gmock_main
.PHONY : gmock_main

# fast build rule for target.
gmock_main/fast:
	$(MAKE) -f Testing/lib/googletest-master/googlemock/CMakeFiles/gmock_main.dir/build.make Testing/lib/googletest-master/googlemock/CMakeFiles/gmock_main.dir/build
.PHONY : gmock_main/fast

#=============================================================================
# Target rules for targets named gmock

# Build rule for target.
gmock: cmake_check_build_system
	$(MAKE) -f CMakeFiles/Makefile2 gmock
.PHONY : gmock

# fast build rule for target.
gmock/fast:
	$(MAKE) -f Testing/lib/googletest-master/googlemock/CMakeFiles/gmock.dir/build.make Testing/lib/googletest-master/googlemock/CMakeFiles/gmock.dir/build
.PHONY : gmock/fast

#=============================================================================
# Target rules for targets named gtest_main

# Build rule for target.
gtest_main: cmake_check_build_system
	$(MAKE) -f CMakeFiles/Makefile2 gtest_main
.PHONY : gtest_main

# fast build rule for target.
gtest_main/fast:
	$(MAKE) -f Testing/lib/googletest-master/googletest/CMakeFiles/gtest_main.dir/build.make Testing/lib/googletest-master/googletest/CMakeFiles/gtest_main.dir/build
.PHONY : gtest_main/fast

#=============================================================================
# Target rules for targets named gtest

# Build rule for target.
gtest: cmake_check_build_system
	$(MAKE) -f CMakeFiles/Makefile2 gtest
.PHONY : gtest

# fast build rule for target.
gtest/fast:
	$(MAKE) -f Testing/lib/googletest-master/googletest/CMakeFiles/gtest.dir/build.make Testing/lib/googletest-master/googletest/CMakeFiles/gtest.dir/build
.PHONY : gtest/fast

ChainOfResponsibility/ChainNodeTest.o: ChainOfResponsibility/ChainNodeTest.cpp.o

.PHONY : ChainOfResponsibility/ChainNodeTest.o

# target to build an object file
ChainOfResponsibility/ChainNodeTest.cpp.o:
	$(MAKE) -f CMakeFiles/SummerOfBrain.dir/build.make CMakeFiles/SummerOfBrain.dir/ChainOfResponsibility/ChainNodeTest.cpp.o
.PHONY : ChainOfResponsibility/ChainNodeTest.cpp.o

ChainOfResponsibility/ChainNodeTest.i: ChainOfResponsibility/ChainNodeTest.cpp.i

.PHONY : ChainOfResponsibility/ChainNodeTest.i

# target to preprocess a source file
ChainOfResponsibility/ChainNodeTest.cpp.i:
	$(MAKE) -f CMakeFiles/SummerOfBrain.dir/build.make CMakeFiles/SummerOfBrain.dir/ChainOfResponsibility/ChainNodeTest.cpp.i
.PHONY : ChainOfResponsibility/ChainNodeTest.cpp.i

ChainOfResponsibility/ChainNodeTest.s: ChainOfResponsibility/ChainNodeTest.cpp.s

.PHONY : ChainOfResponsibility/ChainNodeTest.s

# target to generate assembly for a file
ChainOfResponsibility/ChainNodeTest.cpp.s:
	$(MAKE) -f CMakeFiles/SummerOfBrain.dir/build.make CMakeFiles/SummerOfBrain.dir/ChainOfResponsibility/ChainNodeTest.cpp.s
.PHONY : ChainOfResponsibility/ChainNodeTest.cpp.s

ChainOfResponsibility/Dog.o: ChainOfResponsibility/Dog.cpp.o

.PHONY : ChainOfResponsibility/Dog.o

# target to build an object file
ChainOfResponsibility/Dog.cpp.o:
	$(MAKE) -f CMakeFiles/SummerOfBrain.dir/build.make CMakeFiles/SummerOfBrain.dir/ChainOfResponsibility/Dog.cpp.o
.PHONY : ChainOfResponsibility/Dog.cpp.o

ChainOfResponsibility/Dog.i: ChainOfResponsibility/Dog.cpp.i

.PHONY : ChainOfResponsibility/Dog.i

# target to preprocess a source file
ChainOfResponsibility/Dog.cpp.i:
	$(MAKE) -f CMakeFiles/SummerOfBrain.dir/build.make CMakeFiles/SummerOfBrain.dir/ChainOfResponsibility/Dog.cpp.i
.PHONY : ChainOfResponsibility/Dog.cpp.i

ChainOfResponsibility/Dog.s: ChainOfResponsibility/Dog.cpp.s

.PHONY : ChainOfResponsibility/Dog.s

# target to generate assembly for a file
ChainOfResponsibility/Dog.cpp.s:
	$(MAKE) -f CMakeFiles/SummerOfBrain.dir/build.make CMakeFiles/SummerOfBrain.dir/ChainOfResponsibility/Dog.cpp.s
.PHONY : ChainOfResponsibility/Dog.cpp.s

ChainOfResponsibility/Fish.o: ChainOfResponsibility/Fish.cpp.o

.PHONY : ChainOfResponsibility/Fish.o

# target to build an object file
ChainOfResponsibility/Fish.cpp.o:
	$(MAKE) -f CMakeFiles/SummerOfBrain.dir/build.make CMakeFiles/SummerOfBrain.dir/ChainOfResponsibility/Fish.cpp.o
.PHONY : ChainOfResponsibility/Fish.cpp.o

ChainOfResponsibility/Fish.i: ChainOfResponsibility/Fish.cpp.i

.PHONY : ChainOfResponsibility/Fish.i

# target to preprocess a source file
ChainOfResponsibility/Fish.cpp.i:
	$(MAKE) -f CMakeFiles/SummerOfBrain.dir/build.make CMakeFiles/SummerOfBrain.dir/ChainOfResponsibility/Fish.cpp.i
.PHONY : ChainOfResponsibility/Fish.cpp.i

ChainOfResponsibility/Fish.s: ChainOfResponsibility/Fish.cpp.s

.PHONY : ChainOfResponsibility/Fish.s

# target to generate assembly for a file
ChainOfResponsibility/Fish.cpp.s:
	$(MAKE) -f CMakeFiles/SummerOfBrain.dir/build.make CMakeFiles/SummerOfBrain.dir/ChainOfResponsibility/Fish.cpp.s
.PHONY : ChainOfResponsibility/Fish.cpp.s

# Help Target
help:
	@echo "The following are some of the valid targets for this Makefile:"
	@echo "... all (the default if no target is provided)"
	@echo "... clean"
	@echo "... depend"
	@echo "... install/strip"
	@echo "... install/local"
	@echo "... test"
	@echo "... list_install_components"
	@echo "... edit_cache"
	@echo "... SummerOfBrain"
	@echo "... rebuild_cache"
	@echo "... install"
	@echo "... gmock_main"
	@echo "... gmock"
	@echo "... gtest_main"
	@echo "... gtest"
	@echo "... ChainOfResponsibility/ChainNodeTest.o"
	@echo "... ChainOfResponsibility/ChainNodeTest.i"
	@echo "... ChainOfResponsibility/ChainNodeTest.s"
	@echo "... ChainOfResponsibility/Dog.o"
	@echo "... ChainOfResponsibility/Dog.i"
	@echo "... ChainOfResponsibility/Dog.s"
	@echo "... ChainOfResponsibility/Fish.o"
	@echo "... ChainOfResponsibility/Fish.i"
	@echo "... ChainOfResponsibility/Fish.s"
.PHONY : help



#=============================================================================
# Special targets to cleanup operation of make.

# Special rule to run CMake to check the build system integrity.
# No rule that depends on this can have commands that come from listfiles
# because they might be regenerated.
cmake_check_build_system:
	$(CMAKE_COMMAND) -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 0
.PHONY : cmake_check_build_system
