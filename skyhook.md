# Running Coffea processors with data read from CephFS using the Arrow Datasets API.

We added a new executor API called the `run_rados_parquet_job` that allows reading columns out of  Parquet files stored in CephFS by pushing down projection operations into the storage backend.

# Getting Started

**NOTE:** Please make sure that [Docker](https://www.docker.com/) is installed and running.

1. Install the [Popper](https://github.com/getpopper/popper) container-native workflow engine.

```bash
curl -sSfL https://raw.githubusercontent.com/getpopper/popper/master/install.sh | sh
```

2. Run a single step workflow. Running the workflow will create a single-node Ceph cluster in a Docker container, mount CephFS, and will open up a Jupyter Notebook with a getting started notebook.

```bash
popper run -f wf.yml
```

3. The notebook based guide starts with a brief hands-on on PyArrow with the   `RadosParquetFileFormat` API and then shows how to read data into coffea processors from CephFS by
  doing projection pushdowns using the Arrow Dataset API.
