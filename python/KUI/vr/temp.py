def train_data(self):
    labeled_data = self.read_truth_dsv(self.train_dir)
    n_samples = len(labeled_data)
    img_file = self.train_dir + '/' + labeled_data[0][0]
    image = Image.open(img_file)
    np_img = np.array(image).flatten()
    self.n_features = len(np_img)
    # sample values
    X = np.empty((n_samples, self.n_features), dtype=int)
    # target values = classes
    y = np.empty(n_samples, dtype=int)
    s = 0
    for l_d in labeled_data:
        img_file = self.train_dir + '/' + l_d[0]
        img_label_ascii = ord(l_d[1])
        image = Image.open(img_file)
        np_img = np.array(image).flatten()
        X[s] = np_img
        y[s] = img_label_ascii
        s += 1
    return X, y

def read_truth_dsv(self, data_dir):
    d_f = Path(data_dir, self.TRUTH_FILE)
    ret = []
    with open(d_f, 'r') as d_f:
        for line in d_f.readlines():
            stripped = line.strip()
            ret.append(stripped.split(":"))
    return ret

def write_dsv_output(self, X):
    prediction = self.predict(X)
    d_f = Path(self.test_dir, self.output_file)
    with open(d_f, 'w') as d_f:
        d_f.write("output")
