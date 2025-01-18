import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


queries = ['aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am', 'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 
           'av', 'aw', 'ax', 'ay', 'az', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bk', 'bl', 'bm', 'bn', 'bo', 'bp', 
           'bq', 'br', 'bs', 'bt', 'bu', 'bv', 'bw', 'bx', 'by', 'bz', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'cg', 'ch', 'ci', 'cj', 'ck', 
           'cl', 'cm', 'cn', 'co', 'cp', 'cq', 'cr', 'cs', 'ct', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'da', 'db', 'dc', 'dd', 'de', 'df', 
           'dg', 'dh', 'di', 'dj', 'dk', 'dl', 'dm', 'dn', 'do', 'dp', 'dq', 'dr', 'ds', 'dt', 'du', 'dv', 'dw', 'dx', 'dy', 'dz', 'ea', 
           'eb', 'ec', 'ed', 'ee', 'ef', 'eg', 'eh', 'ei', 'ej', 'ek', 'el', 'em', 'en', 'eo', 'ep', 'eq', 'er', 'es', 'et', 'eu', 'ev', 
           'ew', 'ex', 'ey', 'ez', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff', 'fg', 'fh', 'fi', 'fj', 'fk', 'fl', 'fm', 'fn', 'fo', 'fp', 'fq', 
           'fr', 'fs', 'ft', 'fu', 'fv', 'fw', 'fx', 'fy', 'fz', 'ga', 'gb', 'gc', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gj', 'gk', 'gl', 
           'gm', 'gn', 'go', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gv', 'gw', 'gx', 'gy', 'gz', 'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'hg', 
           'hh', 'hi', 'hj', 'hk', 'hl', 'hm', 'hn', 'ho', 'hp', 'hq', 'hr', 'hs', 'ht', 'hu', 'hv', 'hw', 'hx', 'hy', 'hz', 'ia', 'ib', 
           'ic', 'id', 'ie', 'if', 'ig', 'ih', 'ii', 'ij', 'ik', 'il', 'im', 'in', 'io', 'ip', 'iq', 'ir', 'is', 'it', 'iu', 'iv', 'iw', 
           'ix', 'iy', 'iz', 'ja', 'jb', 'jc', 'jd', 'je', 'jf', 'jg', 'jh', 'ji', 'jj', 'jk', 'jl', 'jm', 'jn', 'jo', 'jp', 'jq', 'jr', 
           'js', 'jt', 'ju', 'jv', 'jw', 'jx', 'jy', 'jz', 'ka', 'kb', 'kc', 'kd', 'ke', 'kf', 'kg', 'kh', 'ki', 'kj', 'kk', 'kl', 'km', 
           'kn', 'ko', 'kp', 'kq', 'kr', 'ks', 'kt', 'ku', 'kv', 'kw', 'kx', 'ky', 'kz', 'la', 'lb', 'lc', 'ld', 'le', 'lf', 'lg', 'lh',
           'li', 'lj', 'lk', 'll', 'lm', 'ln', 'lo', 'lp', 'lq', 'lr', 'ls', 'lt', 'lu', 'lv', 'lw', 'lx', 'ly', 'lz', 'ma', 'mb', 'mc', 
           'md', 'me', 'mf', 'mg', 'mh', 'mi', 'mj', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 
           'my', 'mz', 'na', 'nb', 'nc', 'nd', 'ne', 'nf', 'ng', 'nh', 'ni', 'nj', 'nk', 'nl', 'nm', 'nn', 'no', 'np', 'nq', 'nr', 'ns',
           'nt', 'nu', 'nv', 'nw', 'nx', 'ny', 'nz', 'oa', 'ob', 'oc', 'od', 'oe', 'of', 'og', 'oh', 'oi', 'oj', 'ok', 'ol', 'om', 'on',
           'oo', 'op', 'oq', 'or', 'os', 'ot', 'ou', 'ov', 'ow', 'ox', 'oy', 'oz', 'pa', 'pb', 'pc', 'pd', 'pe', 'pf', 'pg', 'ph', 'pi',
           'pj', 'pk', 'pl', 'pm', 'pn', 'po', 'pp', 'pq', 'pr', 'ps', 'pt', 'pu', 'pv', 'pw', 'px', 'py', 'pz', 'qa', 'qb', 'qc', 'qd',
           'qe', 'qf', 'qg', 'qh', 'qi', 'qj', 'qk', 'ql', 'qm', 'qn', 'qo', 'qp', 'qq', 'qr', 'qs', 'qt', 'qu', 'qv', 'qw', 'qx', 'qy',
           'qz', 'ra', 'rb', 'rc', 'rd', 're', 'rf', 'rg', 'rh', 'ri', 'rj', 'rk', 'rl', 'rm', 'rn', 'ro', 'rp', 'rq', 'rr', 'rs', 'rt',
           'ru', 'rv', 'rw', 'rx', 'ry', 'rz', 'sa', 'sb', 'sc', 'sd', 'se', 'sf', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so',
           'sp', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'sx', 'sy', 'sz', 'ta', 'tb', 'tc', 'td', 'te', 'tf', 'tg', 'th', 'ti', 'tj',
           'tk', 'tl', 'tm', 'tn', 'to', 'tp', 'tq', 'tr', 'ts', 'tt', 'tu', 'tv', 'tw', 'tx', 'ty', 'tz', 'ua', 'ub', 'uc', 'ud', 'ue',
           'uf', 'ug', 'uh', 'ui', 'uj', 'uk', 'ul', 'um', 'un', 'uo', 'up', 'uq', 'ur', 'us', 'ut', 'uu', 'uv', 'uw', 'ux', 'uy', 'uz',
           'va', 'vb', 'vc', 'vd', 've', 'vf', 'vg', 'vh', 'vi', 'vj', 'vk', 'vl', 'vm', 'vn', 'vo', 'vp', 'vq', 'vr', 'vs', 'vt', 'vu',
           'vv', 'vw', 'vx', 'vy', 'vz', 'wa', 'wb', 'wc', 'wd', 'we', 'wf', 'wg', 'wh', 'wi', 'wj', 'wk', 'wl', 'wm', 'wn', 'wo', 'wp',
           'wq', 'wr', 'ws', 'wt', 'wu', 'wv', 'ww', 'wx', 'wy', 'wz', 'xa', 'xb', 'xc', 'xd', 'xe', 'xf', 'xg', 'xh', 'xi', 'xj', 'xk',
           'xl', 'xm', 'xn', 'xo', 'xp', 'xq', 'xr', 'xs', 'xt', 'xu', 'xv', 'xw', 'xx', 'xy', 'xz', 'ya', 'yb', 'yc', 'yd', 'ye', 'yf',
           'yg', 'yh', 'yi', 'yj', 'yk', 'yl', 'ym', 'yn', 'yo', 'yp', 'yq', 'yr', 'ys', 'yt', 'yu', 'yv', 'yw', 'yx', 'yy', 'yz', 'za',
           'zb', 'zc', 'zd', 'ze', 'zf', 'zg', 'zh', 'zi', 'zj', 'zk', 'zl', 'zm', 'zn', 'zo', 'zp', 'zq', 'zr', 'zs', 'zt', 'zu', 'zv',
           'zw', 'zx', 'zy', 'zz', "John", "Mary", "James", "Sarah", "Robert", "Emily", "Zoey"]

def run_script_in_parallel(queries, chunk_size=10, max_workers=7):
    """
    Processes queries in parallel, dynamically redistributing work to idle threads.
    
    Args:
        queries (list): List of queries to process.
        chunk_size (int): Number of queries per chunk.
        max_workers (int): Number of threads for parallel processing.
    
    Returns:
        list: Combined data from all processed queries.
    """
    session = requests.Session()  # Shared session for all threads
    data = []
    tally = len(queries)
    print(f"Total queries to process: {tally}")

    # Split queries into chunks
    chunks = [queries[i:i + chunk_size] for i in range(0, len(queries), chunk_size)]

    def process_chunk(chunk):
        """Processes a single chunk of queries."""
        chunk_data = []
        for query in chunk:
            print(f"Processing query: {query}")
            try:
                query_response = submit_query(query, session)
                if query_response:
                    user_links = get_user_links(query_response)
                    chunk_data.extend(get_user_data(user_links, session))
                print(f"Finished query: {query}")
            except Exception as e:
                print(f"Error processing query {query}: {e}")
        return chunk_data

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_chunk, chunk): chunk for chunk in chunks}

        for future in as_completed(futures):
            try:
                data.extend(future.result())  # Collect data from completed chunk
                tally -= len(futures[future])
                print(f"Queries remaining: {tally}")
            except Exception as e:
                print(f"Error processing chunk: {e}")

    return data
        

def submit_query(query, session):
    
    data = {"search": query,
            "action": "Search",
            "searchtype": "basic",
            "activetab": "basic"}
    url = 'https://directory.andrew.cmu.edu/index.cgi'
    
    response = session.post(url, data)
    
    if response.status_code == 200:
        return response
    else:
        print("Error getting response, status code:", response.status_code)
        return None

def is_valid(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    user_class = soup.find("h1", {"id": "listing"}).get_text()
    
    return "Student" in user_class or "Faculty" in user_class
    
def get_user_links(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("div", {"class": "table-container"})
    table_anchors = table.find_all("a")
    
    user_links = [anchor.get("href").strip() for anchor in table_anchors]
    base_url = 'https://directory.andrew.cmu.edu/'
    user_links =  [base_url + anchor for anchor in user_links]
    user_links = list(set(user_links))
    
    return user_links
    
def get_user_data(links, session):
    data = []
    for link in links:
        try:
            response = session.get(link)
            if is_valid(response):
                user_data = parse_user_data(response)
                data.append(user_data)
        except Exception as e:
            print(f"Error processing user link '{link}': {e}")
    return data
    
def parse_user_data(user_page):
    soup = BeautifulSoup(user_page.text, 'html.parser')
    content_div = soup.find("div", {"style": "padding-top: 50px;"})
    if not content_div:
        raise ValueError("Content div not found")
    # Get the name
    user_name = content_div.find("h1", {"id": "listing"}).get_text()
    # Get the email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email = re.findall(email_pattern, user_page.text)
    if not email:
        raise ValueError("Email not found")
    return {"Name/Category": user_name, "Email": email[0]}


def main():
    
    data = run_script_in_parallel(queries, 10, 7)
    print(f"Total data collected: {len(data)} records")
    data_df = pd.DataFrame(data)
    data_df.to_excel("cmu_data.xlsx", index=False)
    print("Data saved to cmu_data_parallel.xlsx")
    return

if __name__ == "__main__":
    main()