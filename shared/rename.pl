#! /usr/bin/perl -w
use strict;
use File::Find ();
use File::Basename;
use File::Spec;
use File::Copy;
use File::Path;
use autodie;
use Getopt::Long;
use Cwd;

# Set the variable $File::Find::dont_use_nlink if you're using AFS,
# since AFS cheats.

# for the convenience of &wanted calls, including -eval statements:
use vars qw/*name *dir *prune/;
*name   = *File::Find::name;
*dir    = *File::Find::dir;
*prune  = *File::Find::prune;

sub wanted_file;
sub wanted_dir;
sub remove_file;
sub remove_dir;
sub printd;

my $newfile;
my $dirname_old;
my $basename_old;
my $dirname_new;
my $basename_new;
my $cur_path_old;
my $cur_path_new;
my $cur_file_old;
my $cur_file_new;
my $abs_path_old;
my $abs_path_new;
my $abs_file_old;
my $abs_file_new;
my $prog_path;
my $prog_name;
my $gbase;
my $filename_old;
my ($usage, $help, $debug, $impl_bypass, $from_def);
my $found=0;
#my $to_delete_dir=0;
#my $to_delete_file=0;

$prog_name = basename $0;

#README
$usage =
"Replace abc terms with def terms in both text and filename.
On your root of local repo or path within local repo.
Before running this script, please make sure your repo is clean!
To clean your repo, following git commands can be used:

  git reset HEAD --hard; git clean -d -f; git pull --rebase

Also, remember to source shared/dotcshrc

  cd shared
  source dotcshrc

$prog_name --help         //Show this message
$prog_name                //without debug message but warning message
$prog_name --debug        //with debug message and warning message
$prog_name --impl_bypass  //Bypass any files/folders with implementation terms
                          //By default, the script will remove implementation_tsmc*/*DEF* folder
$prog_name --from_def //under def database, catching ENV DEF_HOME instead of ABC_HOME

";


$help         = '';
$debug        = '';
$impl_bypass  = '';
$from_def     = '';

GetOptions (
  'help'         => \$help,
  'debug'        => \$debug,
  'impl_bypass'  => \$impl_bypass,
  'from_def'     => \$from_def
);

# Traverse desired filesystems
if ($help) {
  print ("$usage\n");
} else {
  my $dt = `date`;
  print ("Start time : $dt\n");
  print ("Processing ...\n");
  my $gst_s = `git status -s`;
  print("git status -s :\n=\n$gst_s=\n");
  if ($gst_s)  {
    print ("CAUTION!!!!: Your git branch is not clean and not up to date\n");
    print ("Please do the following git commands to reset your branch and make your branch up to date\n");
    print ("git reset HEAD --hard; git clean -d -f; git rebase --rebase\n");
    if ($gst_s=~ /^.*(abc2def|($prog_name)).*\z/s) {
      print ("NEVER PUT abc2def script, which is not tracked, under Git base\n");
    }
    exit;
  }

  $prog_path = cwd();

  if ($from_def) {
    $gbase = dirname "$ENV{DEF_HOME}";
  } else {
    $gbase = dirname "$ENV{ABC_HOME}";
  }

  printd("Renaming base : $prog_path\n");
  printd("Git base      : $gbase\n");

 if (!$impl_bypass) {
    system ("rm -rf implementation_tsmc_*/ABC*");
  }

  File::Find::find({wanted => \&wanted_file}, '.'); #replace text from Abc/abc/ABC to Def/def/DEF
                                                    #create file/path from Abc/abc/ABC to Def/def/DEF

  print ("Processed!\n");
  $dt = `date`;
  print ("Time : $dt\n");

  print ("git add -A -f\n");
  system "git add -A -f"; #take all added/modified/removed changes
  $dt = `date`;
  print ("Time : $dt\n");

  print ("git clean -fd\n");
  system "git clean -fd"; #remove empty dir

  $dt = `date`;
  print ("End time : $dt\n");

}
exit;

sub printd {
  if ($debug) {
    print "$_[0]";
  }
}

#cp $newfile to dir($newfile)
sub wanted_file {
    print("name = $name in wanted_file\n"); #name is relative path

    $filename_old = basename $name;
    $abs_path_old = cwd();
    $abs_file_old = File::Spec->catfile($abs_path_old, $filename_old);
    $basename_old = File::Spec->abs2rel($abs_file_old, $gbase);
    $dirname_old  = File::Spec->abs2rel($abs_path_old, $gbase);

    if ($dirname_old =~ /^.*\.git.*\z/s) {
      return;
    }

    if ($impl_bypass) {
      if ($basename_old =~ /^.*(($prog_name)).*\z/s) {
        return;
     } elsif ($basename_old =~ /^.*(svh|txt|README).*\z/s) { #txt/README is the exception
      } elsif ($basename_old =~ /^.*(pdf|docs).*\z/s) {
        return;
      }
    } else {
      if ($basename_old =~ /^.*(($prog_name)).*\z/s) {
        return;
      } elsif ($basename_old =~ /^.*(svh|txt|README).*\z/s) { #txt/README is the exception
      } elsif ($basename_old =~ /^.*(implementation|pdf|docs).*\z/s) {
        return;
      }
    }

  $found = ($basename_old =~ /^.*(abc|Abc|ABC).*\z/s);

  ($basename_new = $basename_old) =~ s/abc/def/g;
  $basename_new =~ s/Abc/Def/g;
  $basename_new =~ s/ABC/DEF/g;
  $abs_file_new = File::Spec->catfile($gbase, $basename_new);
  $abs_path_new = dirname $abs_file_new;

  if (! -l $abs_file_old && -d _ && $found) { #abs_file_new is a directory
    if (! -e $abs_file_new) {
      my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev,
      $size, $atime, $mtime, $ctime, $blksize, $blocks)
      = stat($abs_file_old);
      mkpath("$abs_file_new", 1, $mode);
    }
  } elsif (-l $abs_file_old) { #abs_file_new is a link
    my $link_target = readlink ($abs_file_old);
    #print("$link_target\n");
    my $link_target_found = ($link_target =~ /^.*(abc|Abc|ABC).*\z/s);
    if ($found || $link_target_found) {
      if (! -e $abs_path_new) { #if new fir not existed, mkdir it)
        my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev,
        $size, $atime, $mtime, $ctime, $blksize, $blocks)
        = stat($abs_path_old);
        mkpath("$abs_path_new", 1, $mode);
      }
      unlink $abs_file_old;
      if ($link_target_found) {
        $link_target =~ s/abc/def/g;
        $link_target =~ s/Abc/Def/g;
        $link_target =~ s/ABC/DEF/g;
      }
      symlink $link_target, $abs_file_new;
    }
  } elsif (-f $abs_file_old) { #modify if it is just a file
    if (! -e $abs_path_new) { #if new fir not existed, mkdir it)
      my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev,
      $size, $atime, $mtime, $ctime, $blksize, $blocks)
      = stat($abs_path_old);
      mkpath("$abs_path_new", 1, $mode);
    }

    if (-T $abs_file_old) { #modify only if it is a text file
      my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev,
        $size, $atime, $mtime, $ctime, $blksize, $blocks)
        = stat($abs_file_old);
      rename "$abs_file_old",  "$abs_file_old".'.replace';
      open my $fh_in,  '<', "$abs_file_old".'.replace';
      open my $fh_out, '>', "$abs_file_new";
#      while (<$fh_in>) {
#        s/abc/def/g;
#        s/Abc/Def/g;
#        s/ABC/DEF/g;
#        print $fh_out $_;
#      }
      my $lines = join '', <$fh_in>;
      $line =~ s/abc/def/gm;
      $line =~ s/Abc/Def/gm;
      $line =~ s/ABC/DEF/gm;
      print $fh_out $lines;

      chmod $mode, $abs_file_new;
      unlink "$abs_file_old".'.replace';
      close $fh_in;
      close $fh_out;
    } elsif ($found) { #binary and found
      rename "$abs_file_old",  "$abs_file_new";
    }
  }
}


