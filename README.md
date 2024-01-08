# Image control (`imagectl`)

Tools to manage my image library.

## Features

### Index

Create a index of a directory containing file name, size and hash 

### Organise

Move files to a standard structure based on year and month taken

### Verify

Check integrity of a image collection by comparison with a previously made index

### Deduplicate

Consolidate a second (target) image collection into a reference collection by:

* adding new files found in the target to the reference
  * renaming files if there is a name collision
* removing duplicates from the target collection
