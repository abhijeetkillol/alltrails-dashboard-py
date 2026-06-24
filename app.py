import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="AllTrails Dashboard", page_icon="🥾", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f0f4f0; }
.stat-card { background:white;border-radius:14px;padding:20px 16px;
  box-shadow:0 2px 8px rgba(0,0,0,.07);text-align:center;border-top:4px solid #2E7D32; }
.stat-val { font-size:28px;font-weight:900;color:#2E7D32;line-height:1; }
.stat-lbl { font-size:11px;color:#888;margin-top:6px;text-transform:uppercase;
  letter-spacing:.7px;font-weight:600; }
.stat-sub { font-size:12px;color:#aaa;margin-top:3px; }
</style>""", unsafe_allow_html=True)

TRAILS = [
    {"name":"Index Town Wall Trail","loc":"Index, WA","state":"Washington","type":"Out & Back","dist":2.6,"gain":1243,"diff":"Hard","rating":4.6,"lat":47.8176,"lng":-121.5712},
    {"name":"Talapus Lake Trail","loc":"Snoqualmie Pass, WA","state":"Washington","type":"Out & Back","dist":3.5,"gain":656,"diff":"Easy/Mod","rating":4.7,"lat":47.4012,"lng":-121.5185},
    {"name":"Talapus and Olallie Lakes","loc":"Snoqualmie Pass, WA","state":"Washington","type":"Out & Back","dist":5.8,"gain":1210,"diff":"Easy/Mod","rating":4.7,"lat":47.4012,"lng":-121.5184},
    {"name":"Washington Park Arboretum Loop","loc":"Seattle, WA","state":"Washington","type":"Loop","dist":2.4,"gain":147,"diff":"Easy","rating":4.8,"lat":47.6411,"lng":-122.295},
    {"name":"Azalea Way","loc":"Seattle, WA","state":"Washington","type":"Out & Back","dist":1.4,"gain":22,"diff":"Easy","rating":4.7,"lat":47.6402,"lng":-122.2946},
    {"name":"Trillium Falls Trail","loc":"Orick, CA","state":"California","type":"Loop","dist":2.7,"gain":429,"diff":"Easy/Mod","rating":4.8,"lat":41.3229,"lng":-124.0452},
    {"name":"Lady Bird Johnson Grove Trail","loc":"Orick, CA","state":"California","type":"Loop","dist":1.5,"gain":101,"diff":"Easy","rating":4.8,"lat":41.3032,"lng":-124.0181},
    {"name":"Taylor River Trail","loc":"Snoqualmie Pass, WA","state":"Washington","type":"Out & Back","dist":11.3,"gain":935,"diff":"Easy/Mod","rating":4.4,"lat":47.5608,"lng":-121.5322},
    {"name":"Otter and Big Creek Falls","loc":"Snoqualmie Pass, WA","state":"Washington","type":"Out & Back","dist":9.4,"gain":790,"diff":"Easy/Mod","rating":4.6,"lat":47.561,"lng":-121.5322},
    {"name":"Mailbox Peak Trail","loc":"North Bend, WA","state":"Washington","type":"Out & Back","dist":10.5,"gain":4025,"diff":"Hard","rating":4.7,"lat":47.4666,"lng":-121.6737},
    {"name":"South Tiger Mountain Summit","loc":"Issaquah, WA","state":"Washington","type":"Out & Back","dist":6.6,"gain":1617,"diff":"Easy/Mod","rating":4.4,"lat":47.4427,"lng":-121.9775},
    {"name":"Lime Kiln Trail","loc":"Granite Falls, WA","state":"Washington","type":"Out & Back","dist":6.8,"gain":987,"diff":"Easy/Mod","rating":4.5,"lat":48.0774,"lng":-121.9325},
    {"name":"Rattlesnake Ledge Trail","loc":"North Bend, WA","state":"Washington","type":"Out & Back","dist":5.6,"gain":1466,"diff":"Easy/Mod","rating":4.7,"lat":47.434,"lng":-121.7685},
    {"name":"Whispering Firs & Lloyd Trail Loop","loc":"Snohomish, WA","state":"Washington","type":"Loop","dist":1.8,"gain":91,"diff":"Easy","rating":4.6,"lat":47.7886,"lng":-122.0799},
    {"name":"May's Creek Trail","loc":"Gold Bar, WA","state":"Washington","type":"Out & Back","dist":6.0,"gain":1000,"diff":"Easy/Mod","rating":4.4,"lat":47.8634,"lng":-121.6567},
    {"name":"Granite Lakes Trail","loc":"Snoqualmie Pass, WA","state":"Washington","type":"Out & Back","dist":8.4,"gain":2411,"diff":"Easy/Mod","rating":4.6,"lat":47.4921,"lng":-121.6398},
    {"name":"Twin Falls Trail","loc":"North Bend, WA","state":"Washington","type":"Out & Back","dist":2.6,"gain":587,"diff":"Easy/Mod","rating":4.7,"lat":47.4528,"lng":-121.7054},
    {"name":"Lake Ann Trail (Stehekin)","loc":"Stehekin, WA","state":"Washington","type":"Out & Back","dist":3.5,"gain":705,"diff":"Easy/Mod","rating":4.6,"lat":48.5152,"lng":-120.7359},
    {"name":"Maple Pass Trail","loc":"Winthrop, WA","state":"Washington","type":"Loop","dist":6.8,"gain":2171,"diff":"Hard","rating":4.9,"lat":48.5153,"lng":-120.7358},
    {"name":"Eight Mile to Icicle Creek","loc":"Leavenworth, WA","state":"Washington","type":"Out & Back","dist":6.1,"gain":1276,"diff":"Easy/Mod","rating":4.3,"lat":47.5356,"lng":-120.8131},
    {"name":"Grinnell Glacier Trail","loc":"Siyeh Bend, MT","state":"Montana","type":"Out & Back","dist":11.1,"gain":2047,"diff":"Hard","rating":4.9,"lat":48.7963,"lng":-113.6581},
    {"name":"Lake Josephine North Shore Trail","loc":"Babb, MT","state":"Montana","type":"Out & Back","dist":4.6,"gain":295,"diff":"Easy","rating":4.8,"lat":48.7955,"lng":-113.6575},
    {"name":"Swiftcurrent Nature Trail","loc":"Babb, MT","state":"Montana","type":"Loop","dist":2.6,"gain":131,"diff":"Easy","rating":4.6,"lat":48.7972,"lng":-113.6684},
    {"name":"Wallace Falls & Wallace Lake Loop","loc":"Gold Bar, WA","state":"Washington","type":"Loop","dist":9.4,"gain":1906,"diff":"Hard","rating":4.6,"lat":47.8672,"lng":-121.6787},
    {"name":"Wallace Lake via Woody Trail","loc":"Gold Bar, WA","state":"Washington","type":"Out & Back","dist":9.6,"gain":2017,"diff":"Hard","rating":4.6,"lat":47.867,"lng":-121.6781},
    {"name":"Wallace Falls via Woody Trail","loc":"Gold Bar, WA","state":"Washington","type":"Out & Back","dist":5.2,"gain":1469,"diff":"Easy/Mod","rating":4.8,"lat":47.8669,"lng":-121.678},
    {"name":"Sugarloaf Mountain Trail","loc":"Anacortes, WA","state":"Washington","type":"Out & Back","dist":1.9,"gain":656,"diff":"Easy/Mod","rating":4.7,"lat":48.4678,"lng":-122.6294},
    {"name":"Dirty Harry's Balcony","loc":"North Bend, WA","state":"Washington","type":"Out & Back","dist":4.6,"gain":1381,"diff":"Easy/Mod","rating":4.6,"lat":47.4309,"lng":-121.6322},
    {"name":"Winter Block via Birdhouse Trail","loc":"North Bend, WA","state":"Washington","type":"Out & Back","dist":3.2,"gain":1141,"diff":"Easy/Mod","rating":4.6,"lat":47.4311,"lng":-121.6325},
    {"name":"Poo Poo Point Trail","loc":"Issaquah, WA","state":"Washington","type":"Out & Back","dist":6.9,"gain":1801,"diff":"Easy/Mod","rating":4.7,"lat":47.5194,"lng":-122.0299},
    {"name":"Cable Line Trail to West Tiger #3","loc":"Seattle, WA","state":"Washington","type":"Out & Back","dist":3.2,"gain":2007,"diff":"Hard","rating":4.5,"lat":47.5307,"lng":-121.987},
    {"name":"Icicle Ridge Trail Overlook","loc":"Leavenworth, WA","state":"Washington","type":"Out & Back","dist":5.3,"gain":1758,"diff":"Hard","rating":4.7,"lat":47.5688,"lng":-120.681},
    {"name":"Crescent Beach Trail","loc":"Cannon Beach, OR","state":"Oregon","type":"Out & Back","dist":2.3,"gain":534,"diff":"Easy/Mod","rating":4.7,"lat":45.9194,"lng":-123.9732},
    {"name":"Coldwater Lake via Lakes Trail","loc":"Toutle Lake, WA","state":"Washington","type":"Out & Back","dist":9.0,"gain":767,"diff":"Easy/Mod","rating":4.6,"lat":46.2922,"lng":-122.2662},
    {"name":"Lake Ann Trail (Mt Baker)","loc":"Maple Falls, WA","state":"Washington","type":"Out & Back","dist":8.7,"gain":2047,"diff":"Hard","rating":4.7,"lat":48.8501,"lng":-121.6863},
    {"name":"Snow Lake Trail","loc":"Snoqualmie Pass, WA","state":"Washington","type":"Out & Back","dist":6.7,"gain":1686,"diff":"Easy/Mod","rating":4.7,"lat":47.4454,"lng":-121.4235},
    {"name":"Snow Lake to Source Lake Spur","loc":"Snoqualmie Pass, WA","state":"Washington","type":"Out & Back","dist":4.1,"gain":987,"diff":"Easy/Mod","rating":4.5,"lat":47.4454,"lng":-121.4235},
    {"name":"Colchuck Lake via Stuart Lake Trail","loc":"Leavenworth, WA","state":"Washington","type":"Out & Back","dist":9.1,"gain":2352,"diff":"Hard","rating":4.8,"lat":47.5278,"lng":-120.8208},
    {"name":"Sugarloaf Mtn & Mount Erie Loop","loc":"Anacortes, WA","state":"Washington","type":"Loop","dist":4.5,"gain":1279,"diff":"Easy/Mod","rating":4.7,"lat":48.4678,"lng":-122.6296},
    {"name":"Clayton Beach Trail","loc":"Bellingham, WA","state":"Washington","type":"Out & Back","dist":1.4,"gain":170,"diff":"Easy","rating":4.7,"lat":48.648,"lng":-122.4883},
    {"name":"Dark Hollow Falls Trail","loc":"Stanley, VA","state":"Virginia","type":"Out & Back","dist":1.8,"gain":587,"diff":"Easy/Mod","rating":4.6,"lat":38.5196,"lng":-78.431},
    {"name":"Horseshoe Bend Trail","loc":"Deming, WA","state":"Washington","type":"Out & Back","dist":3.2,"gain":479,"diff":"Easy","rating":4.7,"lat":48.9027,"lng":-121.9116},
]

df = pd.DataFrame(TRAILS)
DIFF_COLORS = {"Easy":"#4CAF50","Easy/Mod":"#FFC107","Hard":"#F44336"}

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1B5E20 0%,#2E7D32 60%,#388E3C 100%);
  color:#fff;padding:18px 28px;border-radius:12px;margin-bottom:20px;display:flex;
  align-items:center;gap:14px;">
  <span style="font-size:32px">🥾</span>
  <div>
    <div style="font-size:22px;font-weight:800">AllTrails Dashboard</div>
    <div style="font-size:13px;opacity:.8;margin-top:2px">abhijeet-killol · All completed hikes</div>
  </div>
</div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Stats", "🗺️ Map", "📈 Charts", "📋 Trails"])

# ── STATS ────────────────────────────────────────────────────────────────────
with tab1:
    total_dist = df["dist"].sum()
    total_gain = df["gain"].sum()
    avg_rating = df["rating"].mean()
    states = sorted(df["state"].unique())
    abbr = {"Washington":"WA","California":"CA","Montana":"MT","Oregon":"OR","Virginia":"VA"}

    cols = st.columns(5)
    for col, (val, lbl, sub) in zip(cols, [
        (str(len(df)), "Trails Completed", "Total hikes"),
        (f"{total_dist:.1f} mi", "Total Distance", f"{total_dist*1.609:.0f} km"),
        (f"{total_gain:,} ft", "Elevation Gained", f"{round(total_gain*0.3048):,} m"),
        (f"{avg_rating:.2f} ⭐", "Avg Rating", "Out of 5.0"),
        (str(len(states)), "States Explored", " · ".join(abbr.get(s,s) for s in states)),
    ]):
        col.markdown(f'<div class="stat-card"><div class="stat-val">{val}</div>'
                     f'<div class="stat-lbl">{lbl}</div><div class="stat-sub">{sub}</div></div>',
                     unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        top8 = df.nlargest(8, "gain")
        fig = px.bar(top8, x="gain", y="name", orientation="h", color="diff",
                     color_discrete_map=DIFF_COLORS, title="🏔️ Top 8 Trails by Elevation Gain",
                     labels={"gain":"Elevation Gain (ft)","name":"","diff":"Difficulty"})
        fig.update_layout(yaxis={"categoryorder":"total ascending"},
                          plot_bgcolor="white", paper_bgcolor="white", height=340,
                          legend=dict(orientation="h",yanchor="bottom",y=1.02),
                          margin=dict(l=0,r=10,t=50,b=10))
        fig.update_xaxes(gridcolor="#eee")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        dc = df["diff"].value_counts().reset_index()
        dc.columns = ["Difficulty","Count"]
        fig2 = px.pie(dc, names="Difficulty", values="Count", color="Difficulty",
                      color_discrete_map=DIFF_COLORS, title="🟢 Difficulty Breakdown", hole=0.55)
        fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=340,
                           legend=dict(orientation="h",yanchor="bottom",y=-0.15),
                           margin=dict(l=0,r=0,t=50,b=0))
        st.plotly_chart(fig2, use_container_width=True)

# ── MAP ──────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### 📍 Trail Locations — Interactive US Map")
    fig_map = px.scatter_mapbox(
        df, lat="lat", lon="lng", color="diff", color_discrete_map=DIFF_COLORS,
        size=[8]*len(df), hover_name="name",
        hover_data={"loc":True,"dist":True,"gain":True,"rating":True,"diff":True,"lat":False,"lng":False},
        zoom=5, center={"lat":47.5,"lon":-121.5}, mapbox_style="open-street-map",
        labels={"diff":"Difficulty","dist":"Distance (mi)","gain":"Elev. Gain (ft)","rating":"Rating","loc":"Location"})
    fig_map.update_layout(height=520, margin=dict(l=0,r=0,t=0,b=0),
                          legend=dict(orientation="h",yanchor="bottom",y=1.01,x=0))
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("🟢 Easy  🟡 Easy/Mod  🔴 Hard  |  Scroll to zoom · Drag to pan · Click for details")

# ── CHARTS ───────────────────────────────────────────────────────────────────
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        fig_sc = px.scatter(df, x="dist", y="gain", color="diff", color_discrete_map=DIFF_COLORS,
                            hover_name="name", hover_data={"dist":True,"gain":True,"rating":True,"diff":False},
                            title="📏 Distance vs Elevation Gain",
                            labels={"dist":"Distance (mi)","gain":"Elevation Gain (ft)","diff":"Difficulty"})
        fig_sc.update_traces(marker=dict(size=9, opacity=0.85))
        fig_sc.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=320,
                             legend=dict(orientation="h",yanchor="bottom",y=1.02),
                             margin=dict(l=0,r=0,t=50,b=0))
        fig_sc.update_xaxes(gridcolor="#eee"); fig_sc.update_yaxes(gridcolor="#eee")
        st.plotly_chart(fig_sc, use_container_width=True)
    with c2:
        rc = df["rating"].value_counts().sort_index().reset_index()
        rc.columns = ["Rating","Count"]
        rc["Label"] = rc["Rating"].apply(lambda r: f"⭐ {r:.1f}")
        fig_r = px.bar(rc, x="Label", y="Count", title="⭐ Rating Distribution",
                       labels={"Label":"Rating","Count":"# Trails"},
                       color_discrete_sequence=["#4CAF50"])
        fig_r.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=320,
                            showlegend=False, margin=dict(l=0,r=0,t=50,b=0))
        fig_r.update_yaxes(gridcolor="#eee", dtick=1)
        fig_r.update_xaxes(gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_r, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        sc = df.groupby("state").size().reset_index(name="Count").sort_values("Count", ascending=False)
        fig_st = px.bar(sc, x="state", y="Count", title="🗺️ Trails by State",
                        labels={"state":"State","Count":"# Trails"},
                        color="Count", color_continuous_scale=["#C8E6C9","#1B5E20"])
        fig_st.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=320,
                             showlegend=False, coloraxis_showscale=False,
                             margin=dict(l=0,r=0,t=50,b=0))
        fig_st.update_yaxes(gridcolor="#eee", dtick=2)
        fig_st.update_xaxes(gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_st, use_container_width=True)
    with c4:
        tc = df["type"].value_counts().reset_index(); tc.columns = ["Type","Count"]
        fig_t = px.pie(tc, names="Type", values="Count", title="🔄 Route Type Breakdown", hole=0.5,
                       color_discrete_sequence=["#1B5E20","#2E7D32","#66BB6A"])
        fig_t.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=320,
                            legend=dict(orientation="h",yanchor="bottom",y=-0.2),
                            margin=dict(l=0,r=0,t=50,b=0))
        st.plotly_chart(fig_t, use_container_width=True)

# ── TRAILS TABLE ─────────────────────────────────────────────────────────────
with tab4:
    st.markdown("### 📋 All Trails")
    fc1, fc2, fc3, fc4 = st.columns([3,1,1,1])
    with fc1: search = st.text_input("🔍 Search trails…", placeholder="Name or location")
    with fc2: filt_state = st.selectbox("State", ["All"] + sorted(df["state"].unique().tolist()))
    with fc3: filt_diff = st.selectbox("Difficulty", ["All","Easy","Easy/Mod","Hard"])
    with fc4: sort_by = st.selectbox("Sort by", ["Rating ↓","Distance ↓","Elev. Gain ↓","Name"])

    filtered = df.copy()
    if search:
        q = search.lower()
        filtered = filtered[filtered["name"].str.lower().str.contains(q) | filtered["loc"].str.lower().str.contains(q)]
    if filt_state != "All": filtered = filtered[filtered["state"] == filt_state]
    if filt_diff != "All":  filtered = filtered[filtered["diff"] == filt_diff]
    sort_map = {"Rating ↓":"rating","Distance ↓":"dist","Elev. Gain ↓":"gain","Name":"name"}
    filtered = filtered.sort_values(sort_map[sort_by], ascending=(sort_by=="Name")).reset_index(drop=True)
    filtered.index += 1

    st.caption(f"Showing **{len(filtered)}** of **{len(df)}** trails")
    display = filtered[["name","loc","state","type","dist","gain","diff","rating"]].copy()
    display.columns = ["Trail Name","Location","State","Type","Dist (mi)","Elev. Gain (ft)","Difficulty","Rating"]
    display["Rating"] = display["Rating"].apply(lambda r: f"⭐ {r:.1f}")
    st.dataframe(display, use_container_width=True, height=500)
