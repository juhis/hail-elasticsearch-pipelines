#!/usr/bin/env python

import argparse
import getpass
import os
import socket

p = argparse.ArgumentParser()
p.add_argument("-p", "--project", default="seqr-project")
p.add_argument("-c", "--cluster", default="no-vep")
p.add_argument("script")

args, unknown_args = p.parse_known_args()

#hail_zip="gs://gnomad-bw2/hail-jar/hail-python.prev.zip"
#hail_jar="gs://gnomad-bw2/hail-jar/hail-all-spark.prev.jar"

#hail_zip="gs://gnomad-bw2/hail-jar/hail-python.test.zip"
#hail_jar="gs://gnomad-bw2/hail-jar/hail-all-spark.test.jar"

#hail_zip="gs://gnomad-bw2/hail-jar/hail-python.test2.zip"
#hail_jar="gs://gnomad-bw2/hail-jar/hail-all-spark.test2.jar"

hail_zip="gs://gnomad-bw2/hail-jar/hail-0.1-with-strip-chr-prefix.zip"
hail_jar="gs://gnomad-bw2/hail-jar/hail-0.1-with-strip-chr-prefix.jar"

#hash = subprocess.check_output("gsutil cat gs://hail-common/latest-hash.txt", shell=True).strip()
#hail_zip="gs://hail-common/pyhail-hail-is-master-%(hash)s.zip" % locals()
#hail_jar="gs://hail-common/hail-hail-is-master-all-spark2.0.2-%(hash)s.jar" % locals()

#hash = subprocess.check_output("gsutil cat gs://hail-common/builds/0.1/latest-hash-spark-2.0.2.txt", shell=True).strip()
#hail_zip="gs://hail-common/builds/0.1/python/hail-0.1-%(hash)s.zip" % locals()
#hail_jar="gs://hail-common/builds/0.1/jars/hail-0.1-%(hash)s-Spark-2.0.2.jar" % locals()

#hail_zip="gs://hail-common/0.1-vep-debug.zip"
#hail_jar="gs://hail-common/0.1-vep-debug.jar"



project = args.project
cluster = args.cluster
script = args.script
script_args = " ".join(unknown_args)

if "entire_vds_pipeline" in script:
    username = getpass.getuser()
    directory = "%s:%s" % (socket.gethostname(), os.getcwd())
    script_args += " --username '%(username)s' --directory '%(directory)s'" % locals()

utils_zip = "/tmp/utils.zip"

os.system("zip -r %(utils_zip)s utils" % locals())

command = """gcloud dataproc jobs submit pyspark \
  --project=%(project)s \
  --cluster=%(cluster)s \
  --files=%(hail_jar)s \
  --py-files=%(hail_zip)s,%(utils_zip)s \
  --properties="spark.files=./$(basename %(hail_jar)s),spark.driver.extraClassPath=./$(basename %(hail_jar)s),spark.executor.extraClassPath=./$(basename %(hail_jar)s)" \
  "%(script)s" -- %(script_args)s
""" % locals()

print(command)
os.system(command)
