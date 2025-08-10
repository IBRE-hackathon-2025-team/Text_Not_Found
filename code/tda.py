from sklearn.metrics import pairwise_distances
from gtda.homology import VietorisRipsPersistence
import numpy as np
import pandas as pd
from gtda.plotting import plot_diagram
import plotly.graph_objects as go
import plotly.io as pio



class Topology:
    def read_freq_table(self, filename:str, n_words:int):
        """Read frequencies table made in stylo"""
        freq_dict = {}

        with open(filename, 'r') as file:
            for i,line in enumerate(file):
                line = line.strip()
                if not line:
                    continue
                if (i==0):
                    books = line.replace('"','').split()
                    continue
                if (i == n_words+1):
                    break
                parts = line.split()
                key = parts[0]
                key = key.replace('"',"")
                values = np.array(parts[1:]).astype(float)
                freq_dict[key] = values



        books_freq_vecs = {}


        for j,key in enumerate(freq_dict.keys()):
            for i in range(freq_dict[key].size):
                if (j == 0):
                    books_freq_vecs[books[i]] = []
                books_freq_vecs[books[i]].append(freq_dict[key][i])

        return freq_dict,books_freq_vecs,books
    

    def ps_preprocessing(self, part_speech:pd.DataFrame):
        """Normalize part speeches' freqs by columns and returns dict where keys are filenames and values are lists of freqs"""
        numeric_cols = part_speech.iloc[:, 1:].select_dtypes(include=['number']).columns
        part_speech[numeric_cols] = part_speech[numeric_cols] / part_speech[numeric_cols].sum(axis=0)
        names_freq = part_speech.iloc[:, 1:].to_dict('list')
        return names_freq 

    def remove_outliers(self, names_freq:dict, keys_to_remove: list):
        """Remove filenames which are not considered of analysis"""
        #keys_to_remove = [ '02 Записки счастливой прихожанки.txt',
        # '01 Я очень хочу жить. Мой личный опыт.txt',
        #    '03 Никто из ниоткуда.txt',
        #     '05 Никогда не сдавайся.txt']

        for key in keys_to_remove:
            if key in names_freq:
                del names_freq [key]

        books_list_ps = list(names_freq.keys())

        return names_freq, books_list_ps
    

    def analyze_books_tda(self, freq_dict:dict, books_list:list):
        """Return persistence homology diagram"""
        book_vectors = np.array([freq_dict[book] for book in books_list])
        distance_matrix = pairwise_distances(book_vectors, metric='cosine')
        book_indices = {i: book for i, book in enumerate(books_list)}

        vr = VietorisRipsPersistence(
            metric="precomputed",
            homology_dimensions=[0, 1, 2],
            collapse_edges=True,
            n_jobs=1  
        )

        diagrams = vr.fit_transform(distance_matrix[np.newaxis, :, :])[0]  

        return diagrams, distance_matrix, book_indices
    
    def plot_persistence_diagram(self, diagrams):
        plot_diagram(diagrams)


    def create_interactive_plot(self, diagrams, dist_matrix, book_indices):
        """Plot interactive persistence diagram in browser mode"""
        pio.renderers.default = 'browser'
        hover_info = []
        book_groups = []

        for point in diagrams:
            birth, death, dim = point
            pairs = np.argwhere(np.isclose(dist_matrix, death, atol=0.01))
            books_in_feature = sorted({book_indices[i] for i,j in pairs if i != j})

            hover_info.append(
                f"<b>H{dim} Feature</b><br>"
                f"Birth: {birth:.3f}<br>Death: {death:.3f}<br>"
                f"Persistence: {death-birth:.3f}<br>"
                f"<b>Books ({len(books_in_feature)}):</b> {', '.join(books_in_feature)}"
            )
            book_groups.append(', '.join(books_in_feature))

        fig = go.Figure()

        dim_names = {0: "Connected Components", 1: "Loops", 2: "Voids"}
        colors = {0: '#1f77b4', 1: '#ff7f0e', 2: '#2ca02c'}

        for dim in [0, 1, 2]:
            mask = diagrams[:, 2] == dim
            fig.add_trace(go.Scatter(
                x=diagrams[mask, 0],
                y=diagrams[mask, 1],
                mode='markers',
                marker=dict(size=12, color=colors[dim], opacity=0.8,
                           line=dict(width=1, color='DarkSlateGrey')),
                name=dim_names[dim],
                text=np.array(hover_info)[mask],
                hoverinfo='text',

                customdata=np.array(book_groups, dtype=object)[mask]
            ))

        fig.add_shape(type='line', x0=0, y0=0, x1=1, y1=1,
                     line=dict(color='grey', width=1, dash='dash'))

        fig.update_layout(
            title='<b>Interactive Book Topology Analysis</b><br><i>Click points to see books</i>',
            xaxis_title='Birth (Cosine Distance)',
            yaxis_title='Death (Cosine Distance)',
            showlegend=False,
            hovermode='closest',
            width=900,
            height=700,
            margin=dict(l=150, r=50, b=50, t=100),
            plot_bgcolor='rgba(245,245,245,1)'
        )

        return fig
    
    def get_books_from_coords(self, diagrams, dist_matrix, book_indices, target_birth, target_death, dim, tolerance=0.01):
        """Return books participated in topology feature formation by coords"""
        mask = (
            (np.isclose(diagrams[:, 0], target_birth, atol=tolerance)) & 
            (np.isclose(diagrams[:, 1], target_death, atol=tolerance)) &
            (diagrams[:, 2] == dim)
        )

        if not np.any(mask):
            return "No matching feature found"


        pairs = np.argwhere(np.isclose(dist_matrix, target_death, atol=tolerance))
        unique_books = sorted({book_indices[i] for i,j in pairs if i != j})

        return {
            'birth': target_birth,
            'death': target_death,
            'persistence': target_death - target_birth,
            'dimension': dim,
            'books': unique_books
        }
    
    def get_missing_books(self, result, books_list):
        """Return books not participated in topology feature formation"""
        only_in_books_list = [book for book in books_list if book not in result['books']]
        print("Books only in books_list:", only_in_books_list)
