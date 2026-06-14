import torch
import torch.nn as nn

class DKTModel(nn.Module):
    """
    Modelo DKT minimalista basado en LSTM.
    Autor conceptual: Copilot
    """

    def __init__(self, input_size: int, hidden_size: int = 64):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size

        # One-hot de conceptos → LSTM → prob. de acierto
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.output = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        """
        x: tensor de índices de conceptos, shape (batch, seq_len)
        """
        emb = self.embedding(x)              # (batch, seq_len, hidden)
        out, _ = self.lstm(emb)              # (batch, seq_len, hidden)
        logits = self.output(out)            # (batch, seq_len, 1)
        probs = self.sigmoid(logits).squeeze(-1)  # (batch, seq_len)
        return probs
