#HEALTHCARE




   def compute_metrics(self, p):
        """
        Function to compute different metrices for model training
        """
        predictions, labels = p
        predictions = np.argmax(predictions, axis=2)
        label_list = list(self.TRAIN_LABEL2ID.keys())
        
        # Remove ignored index (special tokens)
        true_predictions = [
            [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]
        true_labels = [
            [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]
        precision = precision_score(true_labels, true_predictions)
        recall = recall_score(true_labels, true_predictions)
        f1 = f1_score(true_labels, true_predictions)

        return {
            "precision": precision,
            "recall": recall,
            "f1": f1
        }
