from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
from app.core.config import settings


class Neo4jService:
    def __init__(self):
        self.driver = None

    def connect(self):
        if not self.driver:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
        return self.driver

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver = None

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        driver = self.connect()
        with driver.session() as session:
            result = session.run("""
                MATCH (j:Job)
                RETURN j.name as name, j.description as description, 
                       j.salary as salary, j.type as type, j.source as source
                ORDER BY j.name
            """)
            jobs = []
            for record in result:
                jobs.append({
                    "name": record["name"],
                    "description": record["description"],
                    "salary": record["salary"],
                    "type": record["type"],
                    "source": record["source"]
                })
            return jobs

    def get_promotion_paths(self, job_name: str) -> Dict[str, Any]:
        driver = self.connect()
        with driver.session() as session:
            result = session.run("""
                MATCH path = (start:Job {name: $job_name})-[:PROMOTES_TO*]->(end:Job)
                RETURN path
            """, job_name=job_name)
            
            nodes = {}
            links = []
            
            for record in result:
                path = record["path"]
                for node in path.nodes:
                    if node.element_id not in nodes:
                        nodes[node.element_id] = {
                            "id": node.element_id,
                            "name": node["name"],
                            "type": node.get("type", "Base"),
                            "description": node.get("description", ""),
                            "salary": node.get("salary", "")
                        }
                
                for rel in path.relationships:
                    links.append({
                        "source": rel.start_node.element_id,
                        "target": rel.end_node.element_id,
                        "type": rel.type
                    })
            
            return {
                "nodes": list(nodes.values()),
                "links": links
            }

    def get_transfer_paths(self, job_name: str) -> Dict[str, Any]:
        driver = self.connect()
        with driver.session() as session:
            result = session.run("""
                MATCH path = (start:Job {name: $job_name})-[:TRANSFERS_TO*]-(end:Job)
                WHERE start <> end
                RETURN path
                LIMIT 20
            """, job_name=job_name)
            
            nodes = {}
            links = []
            
            for record in result:
                path = record["path"]
                for node in path.nodes:
                    if node.element_id not in nodes:
                        nodes[node.element_id] = {
                            "id": node.element_id,
                            "name": node["name"],
                            "type": node.get("type", "Base"),
                            "description": node.get("description", ""),
                            "salary": node.get("salary", "")
                        }
                
                for rel in path.relationships:
                    link_key = f"{rel.start_node.element_id}-{rel.end_node.element_id}"
                    if link_key not in [f"{l['source']}-{l['target']}" for l in links]:
                        links.append({
                            "source": rel.start_node.element_id,
                            "target": rel.end_node.element_id,
                            "type": rel.type
                        })
            
            return {
                "nodes": list(nodes.values()),
                "links": links
            }

    def get_full_career_graph(self, job_name: Optional[str] = None, graph_type: str = "all") -> Dict[str, Any]:
        driver = self.connect()
        with driver.session() as session:
            nodes = {}
            links = []
            
            result = session.run("""
                MATCH (j:Job)
                RETURN j.name as name, j.type as type, j.description as description, j.salary as salary
            """)
            for record in result:
                name = record["name"]
                nodes[name] = {
                    "id": name,
                    "name": name,
                    "type": record["type"] or "Base",
                    "description": record["description"] or "",
                    "salary": record["salary"] or ""
                }
            
            if graph_type == "promotion":
                result = session.run("""
                    MATCH (a:Job)-[r:PROMOTES_TO]->(b:Job)
                    RETURN a.name as source, b.name as target, type(r) as rel_type
                """)
            elif graph_type == "transfer":
                result = session.run("""
                    MATCH (a:Job)-[r:TRANSFERS_TO]->(b:Job)
                    RETURN a.name as source, b.name as target, type(r) as rel_type
                """)
            else:
                result = session.run("""
                    MATCH (a:Job)-[r:PROMOTES_TO|TRANSFERS_TO]->(b:Job)
                    RETURN a.name as source, b.name as target, type(r) as rel_type
                """)
            
            for record in result:
                links.append({
                    "source": record["source"],
                    "target": record["target"],
                    "type": record["rel_type"]
                })
            
            return {
                "nodes": list(nodes.values()),
                "links": links
            }

    def get_jobs_with_paths(self) -> List[Dict[str, Any]]:
        driver = self.connect()
        with driver.session() as session:
            result = session.run("""
                MATCH (j:Job)
                OPTIONAL MATCH (j)-[:PROMOTES_TO]->(promo:Job)
                OPTIONAL MATCH (j)-[:TRANSFERS_TO]-(transfer:Job)
                WITH j, count(DISTINCT promo) as promo_count, count(DISTINCT transfer) as transfer_count
                WHERE promo_count > 0 OR transfer_count > 0
                RETURN j.name as name, j.type as type, promo_count, transfer_count
                ORDER BY promo_count DESC, transfer_count DESC
            """)
            
            jobs = []
            for record in result:
                jobs.append({
                    "name": record["name"],
                    "type": record["type"],
                    "promotion_count": record["promo_count"],
                    "transfer_count": record["transfer_count"]
                })
            return jobs


neo4j_service = Neo4jService()
