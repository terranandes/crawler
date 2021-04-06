#! /usr/bin/perl -w
use autodie;
use strict;

my @config_all = qw /
                     erf
                    /;

foreach my $config (@config_all) {
#test
#compile ASM
#chdir "$ENV{HOME}/../logical/testbench/execution_tb/tests/benchmarking/asm";
	#  system "\\cp -f $config.s test.s";
	#system "submit +arm/armcc/6.14 make test";
system "ls";
}
#
