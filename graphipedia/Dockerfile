FROM neo4j:3.4.6

WORKDIR /
RUN apk add --update \
    git \
    wget \
    openjdk8 \
    maven && \
    git clone https://github.com/mirkonasato/graphipedia.git

WORKDIR /graphipedia/
RUN wget -q https://dumps.wikimedia.your.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
RUN sed -i -e 's/<neo4j\.version>.*<\/neo4j\.version>/<neo4j.version>3.4.6<\/neo4j.version>/g' pom.xml
RUN mkdir -p /data/databases/graph.db && mvn package && \
    cp graphipedia-dataimport/target/graphipedia-dataimport.jar ./
RUN bzip2 -dc enwiki-latest-pages-articles.xml.bz2 | \
    java -classpath graphipedia-dataimport.jar \
    org.graphipedia.dataimport.ExtractLinks - enwiki-links.xml
RUN java -Xmx8G -classpath graphipedia-dataimport.jar \
    org.graphipedia.dataimport.neo4j.ImportGraph \
    enwiki-links.xml \
    graphdb
RUN rm -r /var/lib/neo4j/data
RUN mkdir -p /var/lib/neo4j/data/databases/graph.db && \
    mv /graphipedia/graphdb/* /var/lib/neo4j/data/databases/graph.db && \
    chown -R neo4j:neo4j /var/lib/neo4j/data
#RUN mkdir -p /data/databases/graph.db && \
#cp -R /graphipedia/graphdb/* /data/databases/graph.db
# RUN rm -r /graphipedia

WORKDIR /var/lib/neo4j
