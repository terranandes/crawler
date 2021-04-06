#!bin/sh
#!perl -w
#call perl from PATH
eval 'exec perl -x -S $0 ${1+"$@"}'
    if 0;

use strict;
use Getopt::Long;
use File::Basename;
use Cwd;

#Variables
my (
  $prog,
  $usage
);

chmod(prog == qx/basename $0/);
$useage = "
Usage: $prog
This script will xxxxx
-help : xxx
-noexec: xxx
-i: input toggle
-o : output toggle
";

GetOptions (
  "help" => \$help,
  "noexec" => \$noexec,
  "i=s"    => \$in_file,
  "o=s"    => \$out_file
);

#Print usage message only
if ($help) {
  print $usage;
  exit 1;
}


if (!defined($in_file) || !defined($out_file)) {
  print "Need to define both the input file and output file\n";
  print $usage;
  exit 1;
}

# For each line in the given toggle file if there is a part select, ensure it is in the do file

# Open toggle waiver file
open IN_FILE, "$in_file" or die $!;

# Copy toggle do file to toggle.do.old if it exists
system("cp $out_file ${out_file}.old") if (-e $out_file);

# Open toggle do file for writing
open OUT_FILE, ">$out_file" or die $!;

# For each file in the waiver file
while (<IN_FILE>) {

  # If a line matches 'Design Unit' keep unit name
  if (/Design Unit: (\S*)/) {
    $design_unit = $1;
  } else {
    # For each line that does not match Design Unit,
    #   write out 'coverage exclude -du <unit_name> -togglenode {signal name[part select]}
    #   if the line matches \[[0-9]* to [0-9]*\], ensure signal in do file contains the part select
    if (/waive *- *- *(.*)/) {
      defined($design_unit) or die $!;
      $signal_name = $1;
      if ($signal_name =~ /([.\w]*)\[(\d+) to (\d+)\]/) {
        $signal_name = "${1}[${2}:${3}]";
      }
      print OUT_FILE "coverage exclude -du $design_unit -togglenode {$signal_name}\n";
    }
  }

}

close IN_FILE;
close OUT_FILE;
