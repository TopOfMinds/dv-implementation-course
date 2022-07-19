# Data generation

We generate data using [Synth](https://www.getsynth.com/). Install it using instructions [here](https://www.getsynth.com/download).

## Commands for generating data

```
$ synth generate --collection sales_line --size 1000 --to jsonl:data/sales_line.jsonl e_shop/
$ synth generate --collection customer --size 100 --to jsonl:data/customer.jsonl e_shop/
$ synth generate --collection customer_address --size 100 --to jsonl:data/customer_address.jsonl e_shop/
$ synth generate --collection product --size 100 --to jsonl:data/product.jsonl e_shop/
```

`Synth` seem to be to primitive for our needs as it use a new customer id, product id etc for each sales_line. To makr the data set consistent we need to limit the number of customers.

## Export to BQ

At the moment I just create the lake tables manually and initialize them from my local jsonl files in `data/`. Using `Create table ...` on the `datalake` data set, and then filling inth form with `Create table` from `upload`, `File format: jsonl` and `Auto detetct` on `Schema`.
