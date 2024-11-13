def filter_match(df):
    return df[df['match'] == True]

def filter_quality(df, threshold=1):
    return df[df['quality_score'] >= threshold]

def filter_shot(df, is_zeroshot = None, require_scene = None):
    if is_zeroshot is not None:
        df = df[df['is_zeroshot'] == is_zeroshot]
    if require_scene is not None:
        df = df[df['require_scene'] == require_scene]
    return df

def main_filter(df):
    df = filter_match(df)
    df = filter_quality(df)
    return df