from exploration_agent.nodes.info_refiner import team_refiner
from exploration_agent.nodes.relation_finder import relation_finder
from exploration_agent.nodes.researcher import agent_researcher
from exploration_agent.nodes.unifier import agent_unifier
from exploration_agent.tools.drafts import TableDraft, post_draft
from exploration_agent.tools.neo4j import get_processed_tables
from exploration_agent.tools.sources import (
    get_code_from_confluence,
    get_code_from_gitlab,
    get_db_schema,
    get_person,
    get_teams,
)
from exploration_agent.utils import str2json


def process_tables():
    tables_already_exist = get_processed_tables()
    all_tables = get_db_schema()

    new_tables = set(all_tables) - set(tables_already_exist)

    print(new_tables)

    for table in new_tables:
        print("Curernt table:", table)
        table_description = get_code_from_confluence(table)
        table_code = get_code_from_gitlab(table)

        conf_json = agent_researcher.invoke(input={"table_name": table, "description": table_description})
        conf_json = str2json(conf_json.content)

        gitlab_json = agent_researcher.invoke(input={"table_name": table, "description": table_code})
        gitlab_json = str2json(gitlab_json.content)

        united_json = agent_unifier.invoke(
            input={
                "table_name": table,
                "confluence_json": conf_json,
                "gitlab_json": gitlab_json,
            }
        )
        print("United json:", united_json.content)
        table_data = str2json(united_json.content)
        table_data["name"] = table
        print("Entire table:", table_data.keys())

        all_teams = get_teams()
        check_team = table_data["team"]

        true_team_id = team_refiner.invoke(input={"team_name": check_team, "teams": all_teams})
        true_team_id = str2json(true_team_id.content)
        table_data["team"] = true_team_id["team"] if "team" in true_team_id else None

        sources_tables = relation_finder.invoke(input={"table_name": table, "gitlan_code": table_code})
        sources_tables = str2json(sources_tables.content)

        all_tables_set = set(get_db_schema())

        for table in sources_tables["sources_tables"]:
            if table not in all_tables_set:
                sources_tables["sources_tables"].remove(table)

        table_data["sources_tables"] = sources_tables["sources_tables"] if sources_tables["sources_tables"] else None

        if "email" not in get_person(table_data["responsible_person"]):
            table_data["responsible_person"] = "admin@mts.ru"

        table_draft_data = TableDraft(**table_data)
        post_draft(table=table_draft_data)
