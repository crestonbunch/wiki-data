# Wikipedia Music Recommendations

## Pre-trained model

You can skip the instructions here and just extract `artists.tar.xz` and
`compressed.tar.xz` and use the pre-trained model like so:

    pipenv run cosine "Scorpions (band)" --in compressed.npy

The first parameter should be the name of a Wikipedia article corresponding to
an artist you want recommendations for.

## Getting started

Warning: the system requirements for following this entire pipeline are quite
sizeable. You can use the pre-computed model on any computer, however. 

This will create a neo4j graph from Wikipedia page links, and tag each page
corresponding to an artist on Musicbrainz.

### Create a neo4j graph database in Docker

This step may take a while.

    docker build -t graphipedia ./graphipedia
    docker run -p 7474:7474 -p 7687:7687 --name wiki graphipedia

View the neo4j web interface and set a password

    firefox localhost:7474

Initial password is `neo4j`

### Setup a virtual environment

    pipenv install

### Tag Wikipedia pages in neo4j with matching artists from Musicbrainz

    pipenv run tag --in artists \
        --neo4j_user "$(NEO4J_USER)" \
        --neo4j_pw "$(NEO4J_PASSWORD)"

You can now make queries from the neo4j web interface like

```cypher
MATCH (p0:Page {title: 'Tame Impala'}),
    (p1:Page {title: 'Rammstein'}),
    p = shortestPath((p0)-[:Link*..6]->(p1)) 
WHERE ALL (x IN NODES(p) WHERE x.artist = true)
RETURN p
```
To find shortest paths between artists, using only pages in the path that are 
themselves artists.

Or to find all outgoing links from one artist to another:

```cypher
MATCH (p0:Page {title: 'Michael Jackson'}) 
        -[:Link]-> 
      (p:Page {artist: true}) 
RETURN p0, p
```

### Generate the adjacency matrix

    pipenv run adj --in artists.txt \
        --neo4j_user "$(NEO4J_USER)" \
        --neo4j_pw "$(NEO4J_PASSWORD)"

### Compute all-pairs shortest path

This is by far the most demanding step of the whole process. It requires:

1. A CUDA-compatible graphics card and the Nvidia docker runtime
2. A lot of RAM. My system had 64GB of RAM. You will probably need 32GB at a
   minimum. I optimized apsp.py for speed not memory usage, so you can probably
   find ways to bring memory usage down at the cost of speed.
3. Patience. This can take a while, go to the park and get some fresh air.

Due to a memory leak I believe to happen inside gunrock, the command below
will restart the process using a limit and offset. The command saves
node distances in a text file which approached 100GB on my machine. When the
--build paramater is used, the distance matrix will be created from this saved
text file. 

When I ran this there were less than 100,000 nodes in the graph and
I ran out of 22GB of GPU memory after 50,000 so I split it into two batches, but
you may want to tune batches for your setup.


    docker build -t gunrock ./gunrock
    docker run \
        --runtime nvidia \
        --name apsp \
        --rm \
        -it \
        -v "$(pwd)":/apsp \
        -e "GRAPH_FILE=/apsp/graph.npz" \
        gunrock \
        /usr/bin/python3 /apsp/scripts/apsp.py --offset 0 --limit 50000 && \
        /usr/bin/python3 /apsp/scripts/apsp.py --offset 50000 && \
        /usr/bin/python3 /apsp/scripts/apsp.py --offset 100000 --build

This step uses `np.uint8` dtypes for the output matrix. This is to optimize
memory consumption by using as little memory as possible, but also makes an
assumption that no path is longer than 255 nodes. This is extremely
unlikely to occur.

### Train the model

    pipenv run model

### Use the model

The search command uses the names in 'artists.txt' generated earlier.
Unfortunately this is a list of Wikipedia article titles, not actual band names
so you have to use those as input:

    pipenv run cosine "Scorpions (band)" --in apsp.npy

### Generate an embedding matrix

    pipenv run embed
    pipenv run cosine "Scorpions (band)" --in embeddings.npy

### Generate a compressed matrix

    pipenv run compress
    pipenv run cosine "Scorpions (band)" --in compressed.npy
