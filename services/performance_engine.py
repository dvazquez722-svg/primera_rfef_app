from pathlib import Path

import pandas as pd

from services.performance_dimension import (
    PerformanceDimension
)

from dimensions.load_dimension import (
    build_load_dimension
)

from dimensions.intensity_dimension import (
    build_intensity_dimension
)

from dimensions.response_dimension import (
    build_response_dimension
)

from dimensions.trend_dimension import (
    build_trend_dimension
)

from dimensions.comparison_dimension import (
    build_comparison_dimension
)

from dimensions.availability_dimension import (
    build_availability_dimension
)

# =====================================================
# PERFORMANCE ENGINE
# =====================================================

class PerformanceEngine:

    def __init__(

        self,

        dataframe

    ):

        self.df = dataframe.copy()

        self.player = None

        self.player_df = None

        self.profile = {}

    # =================================================
    # PLAYER
    # =================================================

    def set_player(

        self,

        player

    ):

        self.player = player

        self.player_df = (

            self.df[

                self.df["player"]

                ==

                player

            ]

            .sort_values(

                "date"

            )

            .reset_index(

                drop=True

            )

        )

        return self

    # =================================================
    # BUILD PROFILE
    # =================================================

    def build_player_profile(

        self,

        player

    ):

        self.set_player(

            player

        )

        self.profile = {

            "information": self.build_information(),

            "load": build_load_dimension(

                self.player_df

            ),

            "intensity": build_intensity_dimension(

                self.player_df

            ),

            "response": build_response_dimension(

                self.player_df

            ),

            "trend": build_trend_dimension(

                self.player_df

            ),

            "comparison": build_comparison_dimension(

                self.player_df,

                self.df

            ),

            "availability": build_availability_dimension(

                self.player_df

            )

        }

        return self.profile

    # =================================================
    # INFORMATION
    # =================================================

    def build_information(

        self

    ):

        latest = self.player_df.iloc[-1]

        return {

            "player_id": latest.get(

                "player_id"

            ),

            "player": latest.get(

                "player"

            ),

            "team": latest.get(

                "team"

            ),

            "position": latest.get(

                "position"

            ),

            "season": latest.get(

                "season"

            ),

            "last_session": latest.get(

                "date"

            ),

            "sessions": len(

                self.player_df

            )

        }
    
    # =================================================
    # LOAD
    # =================================================

    def get_load(

        self

    ):

        return self.profile.get(

            "load"

        )

    # =================================================
    # INTENSITY
    # =================================================

    def get_intensity(

        self

    ):

        return self.profile.get(

            "intensity"

        )

    # =================================================
    # RESPONSE
    # =================================================

    def get_response(

        self

    ):

        return self.profile.get(

            "response"

        )

    # =================================================
    # TREND
    # =================================================

    def get_trend(

        self

    ):

        return self.profile.get(

            "trend"

        )

    # =================================================
    # COMPARISON
    # =================================================

    def get_comparison(

        self

    ):

        return self.profile.get(

            "comparison"

        )

    # =================================================
    # AVAILABILITY
    # =================================================

    def get_availability(

        self

    ):

        return self.profile.get(

            "availability"

        )

    # =================================================
    # PLAYER DATA
    # =================================================

    def get_player_dataframe(

        self

    ):

        return self.player_df.copy()

    # =================================================
    # LATEST SESSION
    # =================================================

    def get_latest_session(

        self

    ):

        return self.player_df.iloc[-1]

    # =================================================
    # LAST N SESSIONS
    # =================================================

    def get_last_sessions(

        self,

        n=5

    ):

        return (

            self.player_df

            .tail(

                n

            )

            .reset_index(

                drop=True

            )

        )

    # =================================================
    # EXPORT PROFILE
    # =================================================

    def export_profile(

        self

    ):

        return self.profile

    # =================================================
    # RESET
    # =================================================

    def reset(

        self

    ):

        self.player = None

        self.player_df = None

        self.profile = {}

        return self
    
    # =================================================
    # TEAM
    # =================================================

    def set_team(

        self,

        team

    ):

        self.team = team

        self.team_df = (

            self.df[

                self.df["team"]

                ==

                team

            ]

            .sort_values(

                [

                    "player",

                    "date"

                ]

            )

            .reset_index(

                drop=True

            )

        )

        return self

    # =================================================
    # TEAM PLAYERS
    # =================================================

    def get_team_players(

        self

    ):

        if self.team_df is None:

            return []

        return sorted(

            self.team_df[

                "player"

            ]

            .dropna()

            .unique()

            .tolist()

        )

    # =================================================
    # TEAM DATAFRAME
    # =================================================

    def get_team_dataframe(

        self

    ):

        if self.team_df is None:

            return pd.DataFrame()

        return self.team_df.copy()

    # =================================================
    # TEAM SUMMARY
    # =================================================

    def build_team_summary(

        self

    ):

        if self.team_df is None:

            return {}

        latest = (

            self.team_df

            .sort_values(

                "date"

            )

            .groupby(

                "player"

            )

            .tail(

                1

            )

        )

        return {

            "team": self.team,

            "players": latest["player"].nunique(),

            "sessions": len(

                self.team_df

            ),

            "last_session": latest["date"].max()

        }

    # =================================================
    # AVAILABLE PLAYERS
    # =================================================

    def get_players(

        self

    ):

        return sorted(

            self.df[

                "player"

            ]

            .dropna()

            .unique()

            .tolist()

        )

    # =================================================
    # AVAILABLE TEAMS
    # =================================================

    def get_teams(

        self

    ):

        return sorted(

            self.df[

                "team"

            ]

            .dropna()

            .unique()

            .tolist()

        )

    # =================================================
    # AVAILABLE POSITIONS
    # =================================================

    def get_positions(

        self

    ):

        return sorted(

            self.df[

                "position"

            ]

            .dropna()

            .unique()

            .tolist()

        )

    # =================================================
    # AVAILABLE SEASONS
    # =================================================

    def get_seasons(

        self

    ):

        return sorted(

            self.df[

                "season"

            ]

            .dropna()

            .unique()

            .tolist()

        )
    
    # =================================================
    # TEAM
    # =================================================

    def set_team(

        self,

        team

    ):

        self.team = team

        self.team_df = (

            self.df[

                self.df["team"]

                ==

                team

            ]

            .sort_values(

                [

                    "player",

                    "date"

                ]

            )

            .reset_index(

                drop=True

            )

        )

        return self

    # =================================================
    # TEAM PLAYERS
    # =================================================

    def get_team_players(

        self

    ):

        if self.team_df is None:

            return []

        return sorted(

            self.team_df[

                "player"

            ]

            .dropna()

            .unique()

            .tolist()

        )

    # =================================================
    # TEAM DATAFRAME
    # =================================================

    def get_team_dataframe(

        self

    ):

        if self.team_df is None:

            return pd.DataFrame()

        return self.team_df.copy()

    # =================================================
    # TEAM SUMMARY
    # =================================================

    def build_team_summary(

        self

    ):

        if self.team_df is None:

            return {}

        latest = (

            self.team_df

            .sort_values(

                "date"

            )

            .groupby(

                "player"

            )

            .tail(

                1

            )

        )

        return {

            "team": self.team,

            "players": latest["player"].nunique(),

            "sessions": len(

                self.team_df

            ),

            "last_session": latest["date"].max()

        }

    # =================================================
    # AVAILABLE PLAYERS
    # =================================================

    def get_players(

        self

    ):

        return sorted(

            self.df[

                "player"

            ]

            .dropna()

            .unique()

            .tolist()

        )

    # =================================================
    # AVAILABLE TEAMS
    # =================================================

    def get_teams(

        self

    ):

        return sorted(

            self.df[

                "team"

            ]

            .dropna()

            .unique()

            .tolist()

        )

    # =================================================
    # AVAILABLE POSITIONS
    # =================================================

    def get_positions(

        self

    ):

        return sorted(

            self.df[

                "position"

            ]

            .dropna()

            .unique()

            .tolist()

        )

    # =================================================
    # AVAILABLE SEASONS
    # =================================================

    def get_seasons(

        self

    ):

        return sorted(

            self.df[

                "season"

            ]

            .dropna()

            .unique()

            .tolist()

        )
    
    # =================================================
    # DATASET SUMMARY
    # =================================================

    def dataset_summary(

        self

    ):

        return {

            "players": self.df[

                "player"

            ].nunique(),

            "teams": self.df[

                "team"

            ].nunique(),

            "sessions": len(

                self.df

            ),

            "seasons": self.df[

                "season"

            ].nunique(),

            "first_date": self.df[

                "date"

            ].min(),

            "last_date": self.df[

                "date"

            ].max()

        }

    # =================================================
    # CHECK PLAYER
    # =================================================

    def player_exists(

        self,

        player

    ):

        return player in self.df[

            "player"

        ].unique()

    # =================================================
    # CHECK TEAM
    # =================================================

    def team_exists(

        self,

        team

    ):

        return team in self.df[

            "team"

        ].unique()

    # =================================================
    # FILTER DATE RANGE
    # =================================================

    def filter_dates(

        self,

        start_date,

        end_date

    ):

        return (

            self.df[

                (

                    self.df["date"]

                    >=

                    pd.to_datetime(

                        start_date

                    )

                )

                &

                (

                    self.df["date"]

                    <=

                    pd.to_datetime(

                        end_date

                    )

                )

            ]

            .copy()

        )

    # =================================================
    # FILTER POSITION
    # =================================================

    def filter_position(

        self,

        position

    ):

        return (

            self.df[

                self.df["position"]

                ==

                position

            ]

            .copy()

        )

    # =================================================
    # FILTER TEAM
    # =================================================

    def filter_team(

        self,

        team

    ):

        return (

            self.df[

                self.df["team"]

                ==

                team

            ]

            .copy()

        )

    # =================================================
    # FILTER PLAYER
    # =================================================

    def filter_player(

        self,

        player

    ):

        return (

            self.df[

                self.df["player"]

                ==

                player

            ]

            .copy()

        )

    # =================================================
    # LAST TEAM SESSION
    # =================================================

    def get_last_team_session(

        self,

        team

    ):

        team_df = self.filter_team(

            team

        )

        if team_df.empty:

            return pd.DataFrame()

        latest = team_df[

            "date"

        ].max()

        return (

            team_df[

                team_df["date"]

                ==

                latest

            ]

            .copy()

        )
    
    # =================================================
    # BUILD ALL PLAYERS
    # =================================================

    def build_all_players(

        self

    ):

        profiles = {}

        for player in self.get_players():

            profiles[player] = self.build_player_profile(

                player

            )

        return profiles

    # =================================================
    # BUILD TEAM PROFILES
    # =================================================

    def build_team_profiles(

        self,

        team

    ):

        self.set_team(

            team

        )

        profiles = {}

        for player in self.get_team_players():

            profiles[player] = self.build_player_profile(

                player

            )

        return profiles

    # =================================================
    # LATEST TEAM PROFILES
    # =================================================

    def get_latest_profiles(

        self,

        team

    ):

        profiles = self.build_team_profiles(

            team

        )

        latest = {}

        for player, profile in profiles.items():

            latest[player] = {

                "information": profile["information"],

                "load": profile["load"],

                "intensity": profile["intensity"],

                "response": profile["response"],

                "trend": profile["trend"],

                "comparison": profile["comparison"],

                "availability": profile["availability"]

            }

        return latest

    # =================================================
    # EXPORT TEAM SUMMARY
    # =================================================

    def export_team_summary(

        self,

        team

    ):

        profiles = self.build_team_profiles(

            team

        )

        rows = []

        for player, profile in profiles.items():

            rows.append(

                {

                    "player": profile["information"]["player"],

                    "position": profile["information"]["position"],

                    "sessions": profile["information"]["sessions"],

                    "last_session": profile["information"]["last_session"]

                }

            )

        return pd.DataFrame(

            rows

        )

    # =================================================
    # ENGINE STATUS
    # =================================================

    def status(

        self

    ):

        return {

            "dataset_loaded": self.df is not None,

            "rows": len(

                self.df

            ),

            "columns": len(

                self.df.columns

            ),

            "players": self.df["player"].nunique(),

            "teams": self.df["team"].nunique(),

            "current_player": self.player,

            "current_team": getattr(

                self,

                "team",

                None

            )

        }


# =====================================================
# LOAD ENGINE
# =====================================================

def load_engine(

    dataset_path

):

    df = pd.read_csv(

        dataset_path,

        low_memory=False,

        parse_dates=[

            "date"

        ]

    )

    return PerformanceEngine(

        df

    )


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print(

        "Performance Engine"

    )

    print(

        "Este módulo debe importarse desde Streamlit o desde otros servicios."

    )