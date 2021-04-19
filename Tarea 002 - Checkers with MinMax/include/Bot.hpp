/*
int minmaxalfabeta(Node* PositionN, int depth, bool minmaxing, int alpha, int beta)
{
    //LLEGEMOS HASTA LAS RAMAS O QUE EL JUEGO HAYA TERMINADO
    if (depth == 0 || gameover(*PositionN))
    {
        //RETORNAMOS LA RESTA ENTRE LAS DOS FICHAS
        estaticEvaluation(PositionN->contaPb(), PositionN->contaPr());
    }

    if (minmaxing)
    {
        PositionN->maxEval = -INFI;
        for (int i = 0; i < PositionN->numChilds(); i++)
        {
            PositionN->eval = minmaxalfabeta(&PositionN->childs[i], depth - 1, false, alpha, beta);
            PositionN->maxEval = max(PositionN->eval, PositionN->maxEval);
            alpha = max(alpha, PositionN->eval);
            if (beta <= alpha)
            {
                break;
            }
        }
        return PositionN->maxEval;
    }
    else
    {
        PositionN->minEval = INFI;
        for (int i = 0; i < PositionN->numChilds(); i++)
        {
            PositionN->eval = minmaxalfabeta(&PositionN->childs[i], depth - 1, true, alpha, beta);
            PositionN->minEval = min(PositionN->eval, PositionN->minEval);
            beta = min(beta, PositionN->eval);
        }
        return PositionN->minEval;
    }
}*/