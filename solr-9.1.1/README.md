# Solr
## Links
- [Default Solr Home Directory](server/solr/README.md)
- [Legacy from Team 2022](legacy/README.md)
- [Solr Control Script Reference](https://solr.apache.org/guide/solr/latest/deployment-guide/solr-control-script-reference.html) 
- [Solr Plugin](https://solr.apache.org/guide/solr/latest/configuration-guide/libs.html)
- [Solr Examples](example/README.md)
- [Solr Tutorial](tutorial/solr.md)
- [Solr Configuration files](server/solr/README.md)


## Schemaless Mode
1. Launching solr on the local host
```bash
# Export variable SOLR_HOME
# NB: Be sure to do this properly as this variable will be used by solr to locate the configuration files later
# You can find this value along with other key properties at: http://localhost:8983/solr/#/~java-properties
export SOLR_HOME=<path-to-solr>
cd $SOLR_HOME
# By default, this will start solr on port 8983
# You could also access it: http://localhost:8983/solr/#/
bin/solr start 
```
2. Create new core instance
```bash
cd server/solr/configsets
# Create new core based on the settings in _default
cp -rf _default/. testing
curl -X GET 'http://localhost:8983/solr/admin/cores?action=CREATE&name=testing&instanceDir=server/solr/configsets/testing'
```
3. Dummy fields and automatic-generated schema
```bash
# when a solr core is created, some dummy fields are generated:
curl -X GET 'http://localhost:8983/solr/testing/schema/fields'
# add document to solr
curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/testing/update' --data-binary '
{
  "add": {
    "doc": {
        "content":"Late night with Solr 8.5",
        "likes":10
	}
  }
}'
# get current schema fields
curl -X GET "http://localhost:8983/solr/testing/schema/fields"

# delete a collection
curl -X GET 'http://localhost:8983/solr/admin/cores?action=UNLOAD&core=testing&deleteInstanceDir=true&deleteDataDir=true'
```

## Getting Started with Solr
1. Configuration files
```bash
ls server/solr/configsets
```
2. Create new core instance
> A Solr core represents a single physical index
- In Solr literature, the word *solr collection* is often used to designate an index. However, collection only has a meaning in the context of a solr cluster in which a single index is distributed across multiple server  
- there is one solr home directory set per jetty server, and each solr home directory could host multiple cores per server and each core has a separate directory 
	- coreX/conf: containing a core specific configuratoin file and the actual index
		- A solr core must have a config set which is a set of configuration files, which should at least include `managed-schema` (the main configuration file that governs the idnex structure) and `solrconfig.xml` (the main solr configuration file that defines how a core should behave)
	- coreX/data: include data
```bash
cd server/solr/configsets
# Create new core based on the settings in _default
cp -rf _default/. testing
curl -X GET 'http://localhost:8983/solr/admin/cores?action=CREATE&name=testing&instanceDir=server/solr/configsets/testing'
```
3. Use `post.jar` to post document to the solr folder
```bash
cd example/exampledocs
java -jar -Dc=tech_products post.jar *.xml
```

## Solr Query
1. Request handler
- its job is to process requests that hit the solr server. Each request of type query would be processed by a handler with the name *select*
	- similar, if you go to the document section, there is a request handler called *update* instead
2. q: query parameter
- synatx: <field-name>:<value>
- e.g. `*:*`
- the queries that are executed via query parameter will calculate the relevancy first and then display the result ranked based on relevancy
3. fp: filter query parameter
- synatx: <field-name>:<value>
- it is used to restrict the result set
- Note: filter query doesn't affect the relevance score, and it cache the results which makes them much faster
- e.g. `inStock:true`
4. sort
- used to define the sort field and sort order 
- e.g. `price asc`
5. start, rows
- used to specify which page we want to see
- start defines the starting page for result
- rows restricts the num of rows per page
6. fl: field list
- specify which fields to return for each document in the result
- e.g. `name,price,feature,score`
- note that if too much fields are selected, it will slow down the performance as too much bits in result set are transferred from the internet
7. df: dynamic field
- if we haven't define a q(uery) field (and only defines the value) and didn't define *catch-all* fields pre-defined, then the query will fall back on this field  
8. wt
- specify the format of the returned result
- including: json, xml, python, ruby, php, csv
9. advanced feature:
- including hl(highlighting), facet, etc...

### Solr in application
1. you may have a UI with a search bar which sends HTTP request to solr 
- all the interaction with solr core services such as the query processing are performed with HTTP request
- therefore, solr can be queried with rest clients (e.g. using curl) as well as popular language's native client lib
- every specified query could generate its corresponding url on top for use 

### Understanding dynamic fields
> it allows you to apply the same definition to any fields in the documents simply by panning either a prefix or a suffix pattern
- e.g. `<dynamicField name="*_ss" type="String" indexed="true" stored="true"/>`
1. It helps address some common problems when building search applications
- modeling documents with plenty of fields 
	- e.g. 'nick\_name', 'first\_name', 'last\_name' could all be modeled as '\*\_name'
- adding new indexing sources
	- use dynamic field to include new fields itnroduced by the new documents source without making any changes to the schema XML file

### Understanding copy fields
> it allows you to populate one field from one or more other fields 
1. A common usage is to create a single catch-all field which is served as the default query field when clients don't specify a field to query
- drawback: the indexes would increase considerably
